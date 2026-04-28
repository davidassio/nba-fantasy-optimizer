# NBA Fantasy Lineup Optimizer

## Overview

Python-based optimization engine that generates NBA fantasy lineups by maximizing projected fantasy points under salary cap and roster constraints.

The project applies concepts from applied mathematics, operations research, and data science to a real decision-making problem.

Rather than stopping at prediction, this optimizer converts player projections into actionable lineup decisions under realistic contest rules.

---

## Why This Project

Many data science projects focus only on forecasting outcomes.

This project focuses on **optimization** — selecting the best combination of decisions while satisfying constraints.

NBA fantasy lineup construction is a strong example because it combines:

- constrained optimization
- resource allocation
- tradeoff analysis
- combinatorial decision-making
- sports analytics

---

## Current Version (V2)

Version 2 models a DraftKings-style NBA classic lineup with the following roster slots:

- PG
- SG
- SF
- PF
- C
- G
- F
- UTIL

Current functionality includes:

- salary cap optimization
- slot-based lineup construction
- multi-position player eligibility (ex: PG/SG, PF/C)
- no duplicate player usage
- configurable contest rules
- exact optimization using integer programming

---

## Mathematical Formulation

### Decision Variable

Let:

$$
x_{i,s} =
\begin{cases}
1, & \text{if player } i \text{ is assigned to slot } s \\
0, & \text{otherwise}
\end{cases}
$$

---

### Objective

Maximize projected fantasy points:

$$
\max \sum_{i,s} p_i x_{i,s}
$$

Where:

- $p_i$ = projected fantasy points for player $i$

---

### Subject To

#### Salary Cap

$$
\sum_{i,s} c_i x_{i,s} \leq C
$$

#### Fill Every Slot Exactly Once

$$
\sum_i x_{i,s} = 1 \quad \forall s
$$

#### Use Each Player At Most Once

$$
\sum_s x_{i,s} \leq 1 \quad \forall i
$$

#### Binary Decision Variables

$$
x_{i,s} \in \{0,1\}
$$

Where:

- $c_i$ = player salary
- $C$ = total salary cap

---

## Tech Stack

- Python
- pandas
- PuLP
- CBC Solver
- VSCode
- Git
- GitHub

---

## Example Output

```text
slot   player_name        salary   projected_points
PG     Malik Monk         6200     31.0
SG     Josh Hart          6400     32.4
SF     P.J. Washington    5700     26.9
PF     Naz Reid           5600     28.3
C      Myles Turner       6900     34.2
G      Grayson Allen      5200     24.8
F      RJ Barrett         6100     30.1
UTIL   Zion Williamson    7900     39.4

Total Salary: 50000
Projected Points: 247.1
```

---

## Implementation Highlights

- Designed lineup construction as a binary assignment optimization problem
- Implemented multi-position eligibility and flex roster slots
- Integrated CBC solver on Apple Silicon via Homebrew
- Structured project using a modular `src/` package layout
- Added feasibility-aware optimization workflow

---

## How to Run

```bash
source .venv/bin/activate
PYTHONPATH=src python src/nba_fantasy_optimizer/main.py
```

---

## Version History

- **V1** — Basic optimizer with salary cap + roster size constraints
- **V2** — Slot-assignment optimizer with multi-position eligibility

---

## Roadmap

- [x] V1 Basic lineup optimizer
- [x] V2 Slot-based optimizer
- [ ] V3 Realistic salary / projection calibration
- [ ] V4 Multiple lineup generation
- [ ] V5 Exposure constraints
- [ ] V6 Live NBA data integration
- [ ] V7 Historical backtesting dashboard

---

## What This Project Demonstrates

- integer programming applied to real-world decision problems  
- constraint-based optimization and assignment modeling  
- portfolio optimization and exposure control  
- translating analytical outputs into actionable decisions  
- building scalable and extensible data science systems  

## Advanced Features

### Multi-Lineup Generation

Generates multiple high-quality lineups instead of a single optimal solution, enabling comparison of different roster constructions.

---

### Strategy-Based Optimization

Supports multiple lineup strategies:

- **Overall**: maximize projected points
- **Premium-Heavy**: prioritize high-salary players
- **Balanced**: limit high-salary concentration

---

### Player Exposure Constraints

Limits how often a player can appear across generated lineups.

Example:
- Maximum exposure = 2 out of 3 lineups

This prevents over-reliance on a single player and improves portfolio diversity.

---

### Lineup Diversification

Uses overlap constraints to ensure generated lineups are meaningfully different, rather than minor variations of the same solution.

## Key Insight

Pure projection-based optimization often produces highly similar lineups due to concentrated optimal solutions.

To address this, the optimizer incorporates:

- exposure constraints
- lineup overlap limits
- strategy-based rules

This transforms the system from a single-solution optimizer into a **portfolio-based decision engine**.