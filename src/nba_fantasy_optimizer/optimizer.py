import shutil
from typing import Literal

import pandas as pd
import pulp

from nba_fantasy_optimizer.rules import SALARY_CAP, ROSTER_SLOTS, SLOT_ELIGIBILITY


Strategy = Literal["overall", "premium_heavy", "balanced"]


def is_eligible_for_slot(player_positions: list[str], slot: str) -> bool:
    return len(set(player_positions) & SLOT_ELIGIBILITY[slot]) > 0


def get_premium_player_indices(df: pd.DataFrame, percentile: float = 0.80) -> set[int]:
    threshold = df["salary"].quantile(percentile)
    return set(df[df["salary"] >= threshold].index)


def build_model(
    df: pd.DataFrame,
    salary_cap: int,
    strategy: Strategy,
    premium_percentile: float = 0.80,
):
    model = pulp.LpProblem(f"NBA_Lineup_{strategy}", pulp.LpMaximize)

    x = {}
    for i in df.index:
        for slot in ROSTER_SLOTS:
            if is_eligible_for_slot(df.loc[i, "position_list"], slot):
                x[(i, slot)] = pulp.LpVariable(f"x_{i}_{slot}", cat="Binary")

    # Objective
    model += pulp.lpSum(
        df.loc[i, "projected_points"] * x[(i, slot)]
        for (i, slot) in x
    ), "Total_Projected_Points"

    # Fill every roster slot
    for slot in ROSTER_SLOTS:
        model += pulp.lpSum(
            x[(i, slot)]
            for i in df.index
            if (i, slot) in x
        ) == 1, f"Fill_{slot}"

    # Use each player at most once
    for i in df.index:
        model += pulp.lpSum(
            x[(i, slot)]
            for slot in ROSTER_SLOTS
            if (i, slot) in x
        ) <= 1, f"Use_Player_{i}_At_Most_Once"

    # Salary cap
    model += pulp.lpSum(
        df.loc[i, "salary"] * x[(i, slot)]
        for (i, slot) in x
    ) <= salary_cap, "Salary_Cap"

    # Strategy constraints
    premium_players = get_premium_player_indices(df, premium_percentile)

    premium_selected = pulp.lpSum(
        x[(i, slot)]
        for (i, slot) in x
        if i in premium_players
    )

    if strategy == "premium_heavy":
        model += premium_selected >= 2, "At_Least_Two_Premium_Players"

    elif strategy == "balanced":
        model += premium_selected <= 1, "At_Most_One_Premium_Player"

    elif strategy == "overall":
        pass

    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    return model, x


def extract_lineup(df: pd.DataFrame, x: dict) -> pd.DataFrame:
    lineup_rows = []

    for (i, slot), var in x.items():
        if var.value() == 1:
            lineup_rows.append({
                "slot": slot,
                "player_name": df.loc[i, "player_name"],
                "team": df.loc[i, "team"],
                "eligible_positions": df.loc[i, "eligible_positions"],
                "salary": df.loc[i, "salary"],
                "projected_points": df.loc[i, "projected_points"],
            })

    lineup = pd.DataFrame(lineup_rows)

    slot_order = {slot: idx for idx, slot in enumerate(ROSTER_SLOTS)}
    lineup["slot_order"] = lineup["slot"].map(slot_order)
    lineup["value_per_1000"] = lineup["projected_points"] / (lineup["salary"] / 1000)

    return (
        lineup
        .sort_values("slot_order")
        .drop(columns="slot_order")
        .reset_index(drop=True)
    )


def optimize_lineups(
    df: pd.DataFrame,
    salary_cap: int = SALARY_CAP,
    strategy: Strategy = "overall",
    n_lineups: int = 3,
    premium_percentile: float = 0.80,
    max_overlap: int = 6,
    max_player_exposure: int = 2,
) -> list[pd.DataFrame]:
    if len(df) < len(ROSTER_SLOTS):
        raise ValueError(
            f"Not enough players in dataset to fill {len(ROSTER_SLOTS)} roster slots."
        )

    if max_overlap >= len(ROSTER_SLOTS):
        raise ValueError("max_overlap must be less than the number of roster slots.")

    if max_player_exposure > n_lineups:
        raise ValueError("max_player_exposure cannot exceed n_lineups.")

    cbc_path = shutil.which("cbc")
    if cbc_path is None:
        raise RuntimeError("CBC solver not found. Install it with `brew install cbc`.")

    solver = pulp.COIN_CMD(path=cbc_path, msg=False)

    model, x = build_model(
        df=df,
        salary_cap=salary_cap,
        strategy=strategy,
        premium_percentile=premium_percentile,
    )

    lineups = []
    player_exposure_counts = {i: 0 for i in df.index}

    for lineup_num in range(n_lineups):
        # Block players who already hit max exposure.
        for i, count in player_exposure_counts.items():
            if count >= max_player_exposure:
                model += pulp.lpSum(
                    x[(i, slot)]
                    for slot in ROSTER_SLOTS
                    if (i, slot) in x
                ) == 0, f"Block_Player_{i}_Lineup_{lineup_num + 1}"

        status = model.solve(solver)

        if pulp.LpStatus[status] != "Optimal":
            break

        lineup = extract_lineup(df, x)
        lineups.append(lineup)

        selected_player_indices = {
            i for (i, slot), var in x.items() if var.value() == 1
        }

        for i in selected_player_indices:
            player_exposure_counts[i] += 1

        # Also force some lineup-level diversity.
        model += pulp.lpSum(
            x[(i, slot)]
            for (i, slot) in x
            if i in selected_player_indices
        ) <= max_overlap, f"Max_Overlap_Lineup_{lineup_num + 1}"

    return lineups


def optimize_lineup(df: pd.DataFrame, salary_cap: int = SALARY_CAP) -> pd.DataFrame:
    lineups = optimize_lineups(
        df=df,
        salary_cap=salary_cap,
        strategy="overall",
        n_lineups=1,
    )

    if not lineups:
        raise RuntimeError("No feasible lineup found.")

    return lineups[0]