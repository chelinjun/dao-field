# TianDao Seed (天道种子)
**Local-first 5-node conservation kernel — Shared Law × Private State**

*A minimal yet complete prototype of a distributed allocation engine: five nodes competing for flow under a hard zero-sum constraint. Need-driven reallocation routes flow where it's needed, and usage leaves a permanent mark in a private personal layer. Everything runs locally. Everything stays on your machine.*

[中文版 (Chinese)](README_zh.md)

---

## 1. What is this?

TianDao Seed is a minimal working implementation of a concept:

> **Dead Law × Living State = Locally generated difference**

- **Law layer** (`allocate`) is *dead*: a fixed, auditable, training-free conservation flow dynamics. It does not learn. It only executes.
- **State layer** (`x`, `γ`) is *living*: it changes with every interaction, and only with *your* interactions. No other user's seed will look like yours.
- **Identity** is not designed. It is the residual of your personal usage history from the uniform state `[1,1,1,1,1]`. Your `γ` vector is your fingerprint.

## 2. Architecture

```text
tiandao_seed/
  ├── seed.py          # Core kernel: conservation + growth law (The Law)
  ├── app.py           # Zero-dependency Web Shell (Python standard library only)
  ├── index.html       # Single-file UI (vanilla JS, no external libraries)
  ├── start.bat        # Windows one-click launch
  ├── start.sh         # Linux / macOS one-click launch
  ├── .gitignore       # seed_state.json excluded
  └── seed_state.json  # YOUR private state — generated at first run, never committed
```

### 2.1 Law Layer — `allocate()`

Five nodes in a hard conservation ring:

```text
Compute · Data · Task · Memory · Collab
```

Every step:

```text
gen = a · ( x[prev]·(1−x[i]) − x[i]·(1−x[next]) )     # Neighbors: excitation
inh = b · ( x[next2]·(1−x[i]) − x[i]·(1−x[prev2]) )   # Distant nodes: inhibition
drive = need[i]·γ[i] − mean(need·γ)                    # ZERO-SUM need injection
x[i] += dt · ( gen + inh + drive )
Σx = 1                                                 # Hard normalization: zero-sum
```

- **Conservation**: `Σx ≡ 1.0` at *every single step* (the drive term is zero-sum, so the ledger is preserved analytically — verified: 200 steps, max deviation `0.00e+00`). One node's gain is another's loss. This is not a feature; it is the Law.
- **Need injection**: the `NEED` vector (from keyword-matched intent) pushes flow toward whatever the current task requires. Because the drive is zero-sum, boosting a used channel automatically dilutes the idle ones — usage-driven selection without explicit subtraction.
- **Normalization is the hidden mechanism**: because `Σ = 1`, increasing one used channel necessarily shrinks the others. Selection is a side effect of conservation, not a separate rule.

### 2.2 Growth Layer — `γ`

Each use strengthens the chosen channel's gain:

```python
d["g"][idx] = min(d["g"][idx] * 1.08 * 0.995, 8.0)
```

- `× 1.08` — Hebbian term: *fire together, wire together*.
- `× 0.995` — Forgetting term: *use it or lose it*. A mild brake on the slow variable.
- `min(·, 8.0)` — **Hard cap. This is the real safeguard.** Without it, ~200 repeated uses of one intent drives `γ ≈ 4.8 × 10⁶`; the numbers overflow while the ledger (`Σx=1`) still holds. The cap keeps `γ` human-readable and bounded.

> **Two stacked feedback loops, honestly stated.** The `0.995` term alone does *not* create a stable equilibrium: `1.08 × 0.995 = 1.0716 > 1`, so `γ` still climbs monotonically to the cap (reached at ~30 uses vs ~27 without the brake). The cap is what tames it. A true decay equilibrium would need `decay = 1/1.08 ≈ 0.926`, not `0.995`. We keep `0.995` as a gentle brake; the ceiling is the solution.

## 3. How to Run

```bash
# Requirements: Python 3.7+, zero pip dependencies
# Windows
start.bat
# Linux / macOS
./start.sh        # or: python3 app.py
# → Browser auto-opens http://127.0.0.1:8000
```

> **Double-click note / 双击说明:** Double-clicking `start.bat` opens a **black CMD window** — that window *is* the server, leave it open. The browser opens automatically once the port is bound (no race). If the window closes immediately or shows red text, screenshot it and send it over. If port 8000 is taken by a leftover process, the server auto-shifts to 8001/8002… — watch the URL your browser actually opened.
>
> 双击 `start.bat` 会弹出一个**黑色 CMD 窗口**，那就是服务器本身，别关。端口绑好后浏览器会自动打开（不再抢跑）。若窗口瞬间关闭或报红字，把红字截图发我。若 8000 被上次没关干净的进程占用，服务器会自动换到 8001/8002…，注意浏览器实际打开的地址。

Type natural language. The kernel will:

1. Classify your text into an intent (`code` / `mem` / `write` / `collab`) — pure keyword matching (EN + ZH), no neural networks, offline.
2. Reallocate flow across all five nodes (`x`, displayed as `Σ=1.00`).
3. Awaken the channel with the largest flow share.
4. Grow that channel's `γ` — your seed is permanently different from here on.

All state persists in `seed_state.json`. No accounts. No cloud. No telemetry. The HTTP server binds only to `127.0.0.1` — it works completely offline.

## 4. Design Discipline

Deliberately excluded, and why:

| Exclusion | Reason |
|---|---|
| Cloud sync | The entire value of a seed is that it holds state on *your* machine only |
| Login / Accounts | Your machine is your identity; `γ` is your password |
| LLM intent parsing | A seed should be rough. Keyword matching is free, auditable, offline |
| Electron / Vue / Frameworks | The shell is a mouth and eyes, not a brain. ~40 lines of vanilla JS is enough for a mouth |

**Rule: Make the Law bulletproof, then dress it — never the other way around.**

## 5. Design Validation Experiment (with numerical prediction)

Feed the kernel the same intent 200 times and watch `γ(t)` — the project's health check:

- **Without cap (pure `× 1.08`)** → `γ` overflows: `≈2.2` at 10 uses, `≈10` at 30, `≈47` at 50, `≈4.8×10⁶` at 200. The ledger still holds (`Σx=1`), but the parameter explodes and the repeated channel locks in fully (`x → ~0.99`). Numerically ugly, not a crash.
- **With cap `8.0` (+ `0.995` brake)** → `γ` climbs to the cap by **~30 uses** and stays flat at `8.0`; the repeated channel locks in at `x ≈ 0.86` and holds. Bounded, reproducible, alive.

The two curves: one overflows into meaningless numbers, the other saturates into a stable, interpretable state. The difference is **the cap**, not the decay term. Lock-in (one channel dominating) happens in both — and that is the point: *your seed becomes you.* The cap merely keeps the numbers sane.

## 6. Principles (One Page)

The seed implements a set of patterns that recur across all scales:

1. **Difference is the only currency.** Perfect uniformity and perfect periodicity are both zero-difference states. A system only computes by maintaining a gradient.
2. **The pendulum: dispersion → concentration → standardization → commoditization → dispersion.**
3. **The ratchet.** Every cycle of standardization deposits a layer that never rolls back.
4. **Law sediments, difference reborns.** Conservation is dead, shareable, auditable. State is living, local, non-transferable. The next wave of value is not in "compressed LLMs," but in **Dead Law × Private Data**.
5. **No absolute right, but definite wrong.** The Law layer is powerful precisely because it can refuse. A system that dares to say "no" is a system that can be trusted.

## 7. Roadmap (Ordered by priority. Rule: No shells before the Law is correct.)

- [x] Conservation 5-node ring, need-driven
- [x] `γ` growth with decay + cap
- [ ] **`store`** — Memory channel must store *content*, not just weight
- [ ] **`recall`** — The read side of memory
- [ ] **`validate`** — The first tooth: reject non-compliant input
- [ ] Forked skin/theme variants (external, freely modifiable)

## 8. Contributing

Fork it. Tear off `index.html` and replace it with your own skin — the shell is yours. But the kernel is binding: if you modify `allocate`, conservation (`Σx = 1`) must be preserved, the hard cap must be preserved, and the divergence assertions must be left in place. **The Law is dead. The Law is written. The Law is not negotiable.**

## 9. License

MIT — The Law belongs to everyone. The State belongs to you.

---

*The seed does not predict the harvest. It only ensures that whatever grows, grows from your soil.*
