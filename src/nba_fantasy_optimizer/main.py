from pathlib import Path

from nba_fantasy_optimizer.data_loader import load_players
from nba_fantasy_optimizer.optimizer import optimize_lineup
from nba_fantasy_optimizer.rules import SALARY_CAP, ROSTER_SIZE


def main():
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "data" / "raw" / "players_v1.csv"

    df = load_players(csv_path)

    lineup = optimize_lineup(
        df,
        salary_cap=SALARY_CAP,
        roster_size=ROSTER_SIZE
    )

    print("\nOPTIMAL LINEUP:\n")
    print(lineup)

    print("\nTotal Salary:", lineup["salary"].sum())
    print("Projected Points:", lineup["projected_points"].sum())


if __name__ == "__main__":
    main()