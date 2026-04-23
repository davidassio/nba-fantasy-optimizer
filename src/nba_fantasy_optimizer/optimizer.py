import shutil
import pandas as pd
import pulp

from nba_fantasy_optimizer.rules import SALARY_CAP, ROSTER_SLOTS, SLOT_ELIGIBILITY


def is_eligible_for_slot(player_positions: list[str], slot: str) -> bool:
    return len(set(player_positions) & SLOT_ELIGIBILITY[slot]) > 0


def optimize_lineup(df: pd.DataFrame, salary_cap: int = SALARY_CAP) -> pd.DataFrame:
    if len(df) < len(ROSTER_SLOTS):
        raise ValueError(
            f"Not enough players in dataset to fill {len(ROSTER_SLOTS)} roster slots."
        )

    model = pulp.LpProblem("NBA_DraftKings_Lineup", pulp.LpMaximize)

    # Decision variable:
    # x[(i, slot)] = 1 if player i is assigned to roster slot
    x = {}
    for i in df.index:
        for slot in ROSTER_SLOTS:
            if is_eligible_for_slot(df.loc[i, "position_list"], slot):
                x[(i, slot)] = pulp.LpVariable(f"x_{i}_{slot}", cat="Binary")

    # Objective: maximize projected fantasy points
    model += pulp.lpSum(
        df.loc[i, "projected_points"] * x[(i, slot)]
        for (i, slot) in x
    ), "Total_Projected_Points"

    # Fill each roster slot exactly once
    for slot in ROSTER_SLOTS:
        model += pulp.lpSum(
            x[(i, slot)]
            for i in df.index
            if (i, slot) in x
        ) == 1, f"Fill_{slot}"

    # Each player can be used at most once
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

    cbc_path = shutil.which("cbc")
    if cbc_path is None:
        raise RuntimeError("CBC solver not found. Install it with `brew install cbc`.")

    solver = pulp.COIN_CMD(path=cbc_path, msg=False)
    status = model.solve(solver)

    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError(f"Solver failed with status: {pulp.LpStatus[status]}")

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

    return lineup.sort_values("slot_order").drop(columns="slot_order").reset_index(drop=True)