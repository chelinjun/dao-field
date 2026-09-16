# The 5-Node Conservation Kernel

**Push one up, the others pay for it. No `if` statements. No cases. Pure polynomial.**

This repository contains the micro-kernel of **The Principle of World Operation** (a macro-framework for system dynamics). It models a 5-node coupled dynamical system where balance is a property of the flow, not a set of rules.

[👉 **Click here to view the Interactive Demo**](https://chelinjun.github.io/dao-field/dao-field/)

---

## The Core Equation

```text
ẋᵢ = α*x_{i-1}*(1-xᵢ)  - α*xᵢ*(1-x_{i+1})  // generation (cycle) & inhibition (diagonal)
   + β*x_{i+2}*(1-xᵢ)  - β*xᵢ*(1-x_{i-2})  // generation (cycle) & inhibition (diagonal)
   + ε*sin(ωt + 2πi/5)                       // drive (non-zero)

## The Four Testable Conclusions
1. **Conservation:** `Σxᵢ = 1`
2. **Damped Convergence:** `Re λᵢ = -0.691α - 1.809β < 0`
3. **Drive Breaks the Dead Equilibrium:** Linear-response threshold ε* ≈ 0.503.
4. **No Component Reaches Zero:** Coordinate hyperplanes are repelling.

## 📖 The Complete Framework
This micro-kernel corresponds to the macro-framework in the `/docs` folder.
👉 [Read The Principle of World Operation (EN)](docs/README_EN.md)
