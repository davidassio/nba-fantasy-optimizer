# NBA Fantasy Lineup Optimizer

## Overview

Python-based optimization engine that generates NBA fantasy lineups by maximizing projected fantasy points under salary cap and roster constraints.

This project applies concepts from applied mathematics, operations research, and data science to a real decision-making problem.

---

## Why This Project

Many analytics projects stop at prediction.

This project focuses on **optimization** — converting projected outcomes into actionable decisions while respecting real-world constraints.

Fantasy lineup construction is a strong example of:

- constrained optimization
- tradeoff analysis
- resource allocation
- quantitative decision-making

---

## Current Version (V1)

Version 1 uses a local CSV dataset containing:

- player name
- team
- position
- salary
- projected fantasy points

The optimizer selects the highest projected lineup subject to:

- salary cap
- roster size
- binary player selection decisions

---

## Mathematical Formulation

Let:

- $x_i = 1$ if player $i$ is selected
- $x_i = 0$ otherwise

### Objective

$$
\max \sum_i p_i x_i
$$

### Subject to

$$
\sum_i s_i x_i \leq C
$$

$$
\sum_i x_i = R
$$

$$
x_i \in \{0,1\}
$$

Where:

- $p_i$ = projected points
- $s_i$ = salary
- $C$ = salary cap
- $R$ = roster size

---

## Tech Stack

- Python
- pandas
- PuLP
- CBC Solver
- VSCode
- Git

---

## Implementation Highlights

- Installed and configured CBC solver on Apple Silicon via Homebrew
- Added feasibility checks for impossible lineup constraints
- Structured project using a modular `src/` package layout
- Built reusable optimization pipeline using pandas + PuLP

---

## How to Run

```bash
source .venv/bin/activate
PYTHONPATH=src python src/nba_fantasy_optimizer/main.py
```

---

## Example Output

```text
Total Salary: 70000
Projected Points: 348.9
```

---

## Roadmap

- [x] V1 Salary-cap lineup optimizer
- [ ] V2 Positional roster constraints
- [ ] V3 Multi-lineup generation
- [ ] V4 Live NBA data integration
- [ ] V5 Historical backtesting

---

## What This Project Demonstrates

- integer programming in practice
- optimization under constraints
- data pipeline design
- debugging and environment management
- translating analytics into decisions