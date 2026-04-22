# Twin Problem Recipe (domain-general)

A twin problem preserves the **solution technique** while varying surface features.
A problem that looks similar but requires a different method is NOT a twin.

## Invariant (do not change)

- Pattern(s) required (from `course-index/patterns.md`)
- Number of reasoning steps (±1)
- Topic / section being tested
- Difficulty tier

## Variable (change freely)

- Numerical constants
- Variable names
- System specification within the same pattern space:
  - **Algebra/analysis**: 3×3 matrix ↔ 4×4 matrix, specific function ↔ general parametric family
  - **ODE/PDE**: change coefficients, change boundary/initial conditions while keeping order and type
  - **Mechanics**: pendulum ↔ spring, specific $V(x)$ ↔ different $V(x)$ with same symmetry
  - **E&M**: parallel plates ↔ spherical ↔ cylindrical (if Laplace/Poisson structure is preserved)
  - **Quantum**: infinite well ↔ harmonic oscillator (both yield discrete spectrum); delta potential ↔ finite well (both scattering)
  - **Stat mech / thermo**: ideal gas ↔ van der Waals ↔ Clausius, monatomic ↔ diatomic
  - **Linear algebra**: real ↔ complex entries, finite-dim ↔ ℓ² sequence space
  - **Real analysis**: Lebesgue ↔ Riemann, metric space ↔ topological
- Direction of the ask:
  - "derive X" ↔ "verify X satisfies Y"
  - "show X = 0" ↔ "find conditions under which X = 0"
  - "compute for specific case" ↔ "compute for general case and specialize"

## What cannot change

- The core mathematical move
- The conceptual insight being tested

## Quality checklist (before presenting a twin)

1. ✅ The pattern is genuinely required (no easy shortcut).
2. ✅ Final answer is different from the original (literal or symbolic).
3. ✅ The origin problem ID doesn't leak into the twin's prompt.
4. ✅ The answer exists and is well-posed.
5. ✅ If the original had part (a), (b), (c) scaffolding, twin preserves it unless told otherwise.

## Examples of valid twins (course-agnostic)

**Original**: "Prove $\sum_{n=1}^\infty 1/n^2 = \pi^2/6$ using Fourier series of $f(x) = x$ on $[-\pi, \pi]$."
**Valid twin**: "Prove $\sum_{n=1}^\infty 1/n^4 = \pi^4/90$ using Fourier series of $f(x) = x^2$ on $[-\pi, \pi]$."
(Pattern: Parseval's identity applied to a Fourier series.)

**Original**: "Solve $y'' + 4y = \sin(2x)$ with $y(0) = y'(0) = 0$."
**Valid twin**: "Solve $y'' + 9y = \cos(3x)$ with $y(0) = 1, y'(0) = 0$."
(Pattern: undetermined coefficients at resonance.)

**Original**: "A particle of mass $m$ in an infinite square well of width $L$ — find ground-state energy."
**Invalid twin**: "A particle in a harmonic oscillator — find ground-state energy."
→ Different pattern. Infinite well uses standing waves + boundary conditions; HO uses ladder operators or power series. Not a twin, a fresh problem.

**Valid twin**: "A particle of mass $m$ in an infinite square well of width $L$ — find $\langle x^2 \rangle$ in the ground state."
→ Same pattern (solve TISE with hard walls), different observable.

## Twin vs. re-skin detection

A **re-skin** changes only cosmetic surface; a **twin** changes enough that pattern recognition is genuinely tested.

- Changing $x \to y$ in variable names alone = re-skin (not enough).
- Changing numerical values only = weak twin; acceptable for confidence-check but not for rigorous drill.
- Changing the system specification while preserving the pattern = strong twin; use this for actual drilling.

Aim for **strong twins** unless the user specifically requests a lightweight confidence check.
