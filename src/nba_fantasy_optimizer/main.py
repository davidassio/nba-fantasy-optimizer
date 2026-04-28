from pathlib import Path

from nba_fantasy_optimizer.data_loader import load_players
from nba_fantasy_optimizer.optimizer import optimize_lineups
from nba_fantasy_optimizer.rules import SALARY_CAP


def print_lineup(lineup, lineup_number: int) -> None:
    total_salary = lineup["salary"].sum()
    total_projection = lineup["projected_points"].sum()
    remaining_salary = SALARY_CAP - total_salary

    print(f"\nLineup {lineup_number}")
    print(
        lineup[
            [
                "slot",
                "player_name",
                "team",
                "eligible_positions",
                "salary",
                "projected_points",
                "value_per_1000",
            ]
        ].to_string(index=False)
    )

    print(f"Total Salary: {total_salary}")
    print(f"Remaining Salary: {remaining_salary}")
    print(f"Projected Points: {total_projection:.2f}")


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "data" / "raw" / "players_v1.csv"

    players = load_players(csv_path)

    strategies = {
        "Overall": "overall",
        "Premium-Heavy": "premium_heavy",
        "Balanced": "balanced",
    }

    for display_name, strategy in strategies.items():
        print(f"\n=== TOP 3 {display_name.upper()} LINEUPS ===")

        lineups = optimize_lineups(
            df=players,
            strategy=strategy,
            n_lineups=3,
            max_overlap=6,
            max_player_exposure=2,
        )

        if not lineups:
            print("No feasible lineups found.")
            continue

        for idx, lineup in enumerate(lineups, start=1):
            print_lineup(lineup, idx)


if __name__ == "__main__":
    main()