from pathlib import Path

from nba_fantasy_optimizer.data_loader import load_players
from nba_fantasy_optimizer.optimizer import optimize_lineup
from nba_fantasy_optimizer.rules import SALARY_CAP


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "data" / "raw" / "players_v1.csv"

    players = load_players(csv_path)
    lineup = optimize_lineup(players)

    total_salary = lineup["salary"].sum()
    total_projection = lineup["projected_points"].sum()
    remaining_salary = SALARY_CAP - total_salary

    print("\n=== OPTIMAL LINEUP ===\n")
    print(
        lineup[
            ["slot", "player_name", "team", "eligible_positions", "salary", "projected_points", "value_per_1000"]
        ].to_string(index=False)
    )

    print(f"\nTotal Salary: {total_salary}")
    print(f"Remaining Salary: {remaining_salary}")
    print(f"Projected Points: {total_projection:.2f}")


if __name__ == "__main__":
    main()