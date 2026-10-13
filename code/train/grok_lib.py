"""Experiment framework: grokking under controlled coverage and repetition.

Task:  modular addition (a + b) mod p on a tiny transformer.
Input sequence: [a, '+', b, '='] (4 tokens, causal); the model predicts the
answer token at the final position, so the answer never appears in the input.

Data stream: unique set of size coverage * p^2, each example replicated R
times per epoch, either interleaved (fully reshuffled each epoch) or blocked
(R adjacent copies; unique order reshuffled each epoch). Batches of exactly
`batch_size` are drawn from a continuous stream across epoch boundaries, so
every optimization step consumes the same number of examples in all
conditions.

Matched-steps note: at a fixed number of optimization steps T and batch B,
the expected number of exposures of each unique example is B*T/(coverage*p^2),
independent of R. R therefore isolates the temporal clustering of repeated
exposures; coverage moves diversity and per-example dose.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterator

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# ----------------------------------------------------------------------------
# Task
# ----------------------------------------------------------------------------

class ModularAddition:
    """(a + b) mod p expressed as a 4-token sequence [a, '+', b, '=']."""

    def __init__(self, p: int = 23):
        self.p = p
        self.vocab = p + 2                      # digits 0..p-1, '+', '='
        self.plus_idx = p
        self.equals_idx = p + 1
        self.pairs = np.array([(a, b) for a in range(p) for b in range(p)])
        self.labels = (self.pairs.sum(axis=1) % p).astype(np.int64)
        self.encoded = np.stack([
            np.column_stack([self.pairs[:, 0], np.full(len(self.pairs), self.plus_idx),
                             self.pairs[:, 1], np.full(len(self.pairs), self.equals_idx)])
        ]).astype(np.int64)[0]

    def __len__(self) -> int:
        return len(self.pairs)


# ----------------------------------------------------------------------------
# Model
# ----------------------------------------------------------------------------

class Block(nn.Module):
    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, n_heads, batch_first=True)
        self.ln2 = nn.LayerNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, d_model * 4), nn.GELU(), nn.Linear(d_model * 4, d_model)
        )

    def forward(self, x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        h = self.ln1(x)
        attn_out, _ = self.attn(h, h, h, attn_mask=mask, need_weights=False)
        x = x + attn_out
        return x + self.mlp(self.ln2(x))


class TinyTransformer(nn.Module):
    """Causal transformer over the 4-token arithmetic sequences."""

    def __init__(self, vocab: int, d_model: int = 64, n_layers: int = 2,
                 n_heads: int = 4, max_len: int = 4):
        super().__init__()
        self.embed = nn.Embedding(vocab, d_model)
        self.pos = nn.Embedding(max_len, d_model)
        self.blocks = nn.ModuleList(Block(d_model, n_heads) for _ in range(n_layers))
        self.ln_f = nn.LayerNorm(d_model)
        self.unembed = nn.Linear(d_model, vocab)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        T = x.shape[1]
        pos = torch.arange(T, device=x.device)
        h = self.embed(x) + self.pos(pos)[None]
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), 1)
        for blk in self.blocks:
            h = blk(h, mask)
        return self.unembed(self.ln_f(h))


# ----------------------------------------------------------------------------
# Data stream
# ----------------------------------------------------------------------------

def build_epoch(unique_idx: np.ndarray, repetition: int, mode: str,
                rng: np.random.Generator) -> np.ndarray:
    """One epoch of example indices under the requested repetition mode."""
    if repetition == 1:
        return rng.permutation(unique_idx)
    if mode == "blocked":
        order = rng.permutation(unique_idx)
        return np.repeat(order, repetition)          # a,a,a,a, b,b,b,b, ...
    if mode == "interleaved":
        full = np.repeat(unique_idx, repetition)     # then fully shuffled
        return rng.permutation(full)
    raise ValueError(f"unknown mode {mode}")


def stream_epochs(unique_idx: np.ndarray, repetition: int, mode: str,
                   rng: np.random.Generator) -> Iterator[int]:
    while True:
        for i in build_epoch(unique_idx, repetition, mode, rng):
            yield int(i)


def batched_stream(unique_idx: np.ndarray, repetition: int, mode: str,
                   rng: np.random.Generator, batch_size: int) -> Iterator[np.ndarray]:
    it = stream_epochs(unique_idx, repetition, mode, rng)
    while True:
        yield np.fromiter(it, dtype=np.int64, count=batch_size)


# ----------------------------------------------------------------------------
# Training
# ----------------------------------------------------------------------------

@dataclass
class Config:
    p: int = 23
    d_model: int = 64
    n_layers: int = 2
    n_heads: int = 4
    lr: float = 1e-3
    weight_decay: float = 1.0
    batch_size: int = 256
    max_steps: int = 40_000
    eval_every: int = 100
    coverage: float = 0.85           # fraction of unique pairs used for training
    repetition: int = 1
    mode: str = "blocked"            # blocked | interleaved (irrelevant if R=1)
    seed: int = 0
    grok_threshold: float = 0.95     # test accuracy counted as "generalized"
    mem_threshold: float = 0.95      # train accuracy counted as "memorized"
    tag: str = "run"


def weight_l2(model: nn.Module) -> float:
    return float(sum((p.detach() ** 2).sum().item() for p in model.parameters()) ** 0.5)


def run_training(cfg: Config) -> dict:
    torch.manual_seed(cfg.seed)
    rng = np.random.default_rng(cfg.seed)
    task = ModularAddition(cfg.p)
    encoded = torch.from_numpy(task.encoded)
    labels = torch.from_numpy(task.labels)

    n_pairs = len(task)
    n_train = int(round(cfg.coverage * n_pairs))
    perm = rng.permutation(n_pairs)                  # fixed per seed: same unique set across R
    train_idx = np.sort(perm[:n_train])
    test_idx = np.setdiff1d(np.arange(n_pairs), train_idx)

    model = TinyTransformer(task.vocab, cfg.d_model, cfg.n_layers, cfg.n_heads)
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr,
                            weight_decay=cfg.weight_decay, betas=(0.9, 0.98))

    def accuracy(idx: np.ndarray) -> float:
        model.eval()
        with torch.no_grad():
            logits = model(encoded[torch.from_numpy(idx)])
            pred = logits.argmax(dim=-1)[:, -1]     # next-token prediction at final position
            acc = (pred == labels[torch.from_numpy(idx)]).float().mean().item()
        model.train()
        return acc

    history = []
    grok_step = None
    mem_step = None
    t0 = time.time()
    step = 0
    batches = batched_stream(train_idx, cfg.repetition, cfg.mode, rng, cfg.batch_size)

    while step < cfg.max_steps:
        batch = next(batches)
        xb = encoded[torch.from_numpy(batch)]
        yb = labels[torch.from_numpy(batch)]
        logits = model(xb)
        loss = F.cross_entropy(logits[:, -1, :], yb)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        step += 1

        if step % cfg.eval_every == 0 or step == 1:
            tr_acc = accuracy(train_idx)
            te_acc = accuracy(test_idx)
            history.append(
                dict(step=step, train_loss=float(loss.item()),
                     train_acc=tr_acc, test_acc=te_acc, wnorm=weight_l2(model)))
            if mem_step is None and tr_acc >= cfg.mem_threshold:
                mem_step = step
            if grok_step is None and te_acc >= cfg.grok_threshold:
                grok_step = step
                break                            # early stop after generalization

    final = history[-1] if history else {}
    result = dict(
        config=asdict(cfg), n_train_unique=int(n_train), n_test=int(len(test_idx)),
        grok_step=grok_step, mem_step=mem_step,
        final_train_acc=final.get("train_acc"), final_test_acc=final.get("test_acc"),
        final_train_loss=final.get("train_loss"), final_wnorm=final.get("wnorm"),
        steps_run=step, wall_seconds=round(time.time() - t0, 1),
        n_history=len(history),
    )
    return dict(summary=result, history=history)


def save_result(out_dir: Path, payload: dict) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = payload["summary"]["config"]
    name = (f"{cfg['tag']}_C{int(cfg['coverage']*100)}_R{cfg['repetition']}_"
            f"{cfg['mode']}_s{cfg['seed']}.json")
    path = out_dir / name
    path.write_text(json.dumps(payload, indent=1))
    return path
