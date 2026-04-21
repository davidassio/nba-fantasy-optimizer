import shutil
import pandas as pd
import pulp


def optimize_lineup(df: pd.DataFrame, salary_cap: int, roster_size: int) -> pd.DataFrame:
    if len(df) < roster_size:
        raise ValueError(
            f"Not enough players in dataset to fill roster of size {roster_size}."
        )

    min_possible_salary = df["salary"].nsmallest(roster_size).sum()
    if min_possible_salary > salary_cap:
        raise ValueError(
            f"Infeasible setup: cheapest possible {roster_size}-player lineup costs "
            f"{min_possible_salary}, which exceeds salary cap {salary_cap}."
        )

    model = pulp.LpProblem("NBA_Lineup", pulp.LpMaximize)

    player_vars = {
        i: pulp.LpVariable(f"player_{i}", cat="Binary")
        for i in df.index
    }

    model += pulp.lpSum(
        df.loc[i, "projected_points"] * player_vars[i]
        for i in df.index
    )

    model += pulp.lpSum(
        df.loc[i, "salary"] * player_vars[i]
        for i in df.index
    ) <= salary_cap

    model += pulp.lpSum(
        player_vars[i] for i in df.index
    ) == roster_size

    cbc_path = shutil.which("cbc")
    if cbc_path is None:
        raise RuntimeError("CBC solver not found. Install it with `brew install cbc`.")

    solver = pulp.COIN_CMD(path=cbc_path, msg=False)
    status = model.solve(solver)

    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError(f"Solver failed with status: {pulp.LpStatus[status]}")

    chosen = df[
        [player_vars[i].value() == 1 for i in df.index]
    ].copy()

    return chosen