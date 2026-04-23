from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = {
    "player_name",
    "team",
    "eligible_positions",
    "salary",
    "projected_points",
}


def parse_positions(position_str: str) -> list[str]:
    return [pos.strip() for pos in position_str.split("/")]


def load_players(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["salary"] = pd.to_numeric(df["salary"])
    df["projected_points"] = pd.to_numeric(df["projected_points"])
    df["eligible_positions"] = df["eligible_positions"].astype(str)
    df["position_list"] = df["eligible_positions"].apply(parse_positions)

    if (df["salary"] <= 0).any():
        raise ValueError("All salaries must be positive.")

    if df["projected_points"].isna().any():
        raise ValueError("Projected points cannot contain null values.")

    return df