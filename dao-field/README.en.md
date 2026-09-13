# The Ledger & The Spiral

> Five nodes. One ledger. No `if` statements.
> Click a button. Watch it balance itself.

A five-node coupled dynamical system: **generation–inhibition / zero `if` / saturation / sum always equal to 1**.
Demo page: `index.html` (double-click to run, no backend needed).

---

## One Sentence

**Conservation + saturation + periodic drive = structural self-correction.** No branch decisions required; the system converges on its own, brakes on its own, and stays in bounds on its own.

---

## Core Equation

```
ẋᵢ = α·xᵢ₋₁(1−xᵢ) − α·xᵢ(1−xᵢ₊₁)   // generation (cycle)
   + β·xᵢ₊₂(1−xᵢ) − β·xᵢ(1−xᵢ₋₂)   // inhibition (diagonal)
   + ε·sin(ωt + 2πi/5)              // drive (zero-sum)
```

Five nodes, indices mod 5, α, β, ε > 0. Every term is polynomial — **zero branches**.
`(1 − xᵢ)` is the brake: as xᵢ → 1, inflow goes to zero.

---

## Four Conclusions (All Verifiable by Code)

| # | Conclusion | How to verify |
|---|---|---|
| 1 | **Σxᵢ = 1 conserved** | `node check.js` → 5000 steps, deviation 2.2×10⁻¹⁶ |
| 2 | **Re λ₁ = −0.691α − 1.809β < 0** | α=1, β=0.6 → **−1.776**; `node check.js` |
| 3 | **Drive breaks the dead equilibrium** | Linear threshold **ε* ≈ 0.503**; beyond it, saturation caps amplitude |
| 4 | **No component tends to zero** | 10000 steps, x_min ≈ 6.3×10⁻² |

### How to Run

```bash
npm install   # no dependencies, local script only
npm run check # runs check.js, outputs verification of the four conclusions
```

Or simply `node check.js`.

---

## Why There Is No `if`

Saturation is `(1 − xᵢ)` — plain multiplication.
As xᵢ → 1, inflow goes to zero; as xᵢ → 0, inflow is maximal. **The system brakes itself, without a single branch instruction.**

> **Balance as a property of the flow, not a set of rules.**

---

## Two Shells (Core Mechanism)

```
Shell One: generation–inhibition (conservation)
  → extremes are pushed back to the center

Shell Two: extremes reverse · nadirs rebound (saturation + negative real part)
  → the center itself is a dissipator (dead point)
```

**Shell one prevents you from crossing the boundary; shell two prevents you from stopping at the unique fixed point inside.**

Result: **step out and you're pushed back; stand still and you're worn away.**
There is no point in state space where you can linger — the only two openings left are **two seams**:

- **Seam 1**: δ drive term (external injection) → a closed system must die
- **Seam 2**: slow variable (total K or coupling strength with its own dynamics) → like the sun dying, fuel depletion, K(t) decay

> The only secret for staying alive: **never fully shut the door, and never let yourself return to an absolute 50-50.**

---

## On Verification

Reliability rests on three independent foundations:

1. First-principles equation
2. Conservation invariant (Σxᵢ ≡ 1)
3. Reproducible numerical verification (`node check.js`)

Conclusions have been confirmed by external independent review; some derivations reference public materials, acknowledged here. Detailed self-checks and notes are in [AUDIT.md](./AUDIT.md).

---

## Heaven's Way · Human Way · Reachability of 50-50

| Layer | Mechanism | Reaches 50-50? |
|---|---|---|
| Heaven's Way | More → reduce, less → increase (negative feedback) | ✅ Can (slowly) |
| Human Way | Incomplete and diverse; rob the insufficient to serve the surplus (positive feedback) | ❌ Must tend to extremes |
| Fast resonance | Millisecond-level more → reduce / less → increase | ⚠️ Can, but achieving it is death |

**Existence probability estimate: P ~ 10⁻³** (product of five necessary conditions; see Section 8 of AUDIT.md).

---

## What This Is Not

- Not a theory of everything
- Not a prediction engine
- Not a claim corresponding to any specific tradition (the nodes are just called A–E)

---

## File Structure

```
dao-field/
├── index.html     # interactive demo (double-click to open)
├── check.js       # numerical verification script
├── package.json   # npm run check
├── README.md      # 中文说明
├── README.en.md   # this file
└── AUDIT.md       # full audit and verification notes (bilingual)
```

---

*The ledger is conserved; the spectrum contracts; the drive wakes without spending.*
