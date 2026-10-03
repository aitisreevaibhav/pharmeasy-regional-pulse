import json
import sqlite3
from pathlib import Path

DB_PATH = "pharmeasy.db"
STATE_PATH = "metrics_state.json"


def compute_percentage_change_v1(current, previous):
    """Calculate percentage change and safely handle division by zero."""
    if previous == 0:
        return 0

    return ((current - previous) / previous) * 100


def flag_significant_regions_v1(changes, threshold=8):
    """
    Flag regions whose absolute percentage change
    exceeds the supplied threshold.
    """
    flagged = []

    for region, change in changes.items():
        if abs(change) > threshold:
            flagged.append(region)

    return flagged


def save_state_v1(month_summary, path):
    """Save a month's computed summary as JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(month_summary, f, indent=2)


def load_previous_state_v1(path):
    """Load the previously saved monthly summary."""
    path = Path(path)

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_monthly_sales():
    """Read region/month sales from SQLite."""
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            region,
            substr(order_date, 1, 7) AS month,
            ROUND(SUM(sales_inr), 2) AS total_sales_inr
        FROM orders_clean
        GROUP BY region, month
        ORDER BY region, month;
    """

    rows = conn.execute(query).fetchall()
    conn.close()

    return rows


def build_month_summary(rows):
    """Convert SQL results into a region -> month -> sales dictionary."""
    summary = {}

    for region, month, sales in rows:
        if region not in summary:
            summary[region] = {}

        summary[region][month] = float(sales)

    return summary


def calculate_changes(summary, previous_month, current_month):
    """Calculate MoM percentage changes for every active region."""
    changes = {}

    for region, months in summary.items():
        previous = months.get(previous_month, 0)
        current = months.get(current_month, 0)

        changes[region] = round(
            compute_percentage_change_v1(current, previous),
            2
        )

    return changes


def print_changes(title, changes, flagged):
    print(f"\n=== {title} ===")

    for region in sorted(changes):
        change = changes[region]
        flag = "FLAGGED" if region in flagged else "not flagged"

        print(
            f"{region}: {change:.2f}% -> {flag}"
        )

    print("\nFlagged regions:")

    for region in flagged:
        print(region)


def main():
    rows = get_monthly_sales()

    summary = build_month_summary(rows)

    print("=== MONTHLY SALES SUMMARY ===")

    for region in sorted(summary):
        print(region, summary[region])

    # April -> May
    april_may_changes = calculate_changes(
        summary,
        "2026-04",
        "2026-05"
    )

    april_may_flagged = flag_significant_regions_v1(
        april_may_changes,
        threshold=8
    )

    print_changes(
        "APRIL -> MAY",
        april_may_changes,
        april_may_flagged
    )

    # May -> June
    may_june_changes = calculate_changes(
        summary,
        "2026-05",
        "2026-06"
    )

    may_june_flagged = flag_significant_regions_v1(
        may_june_changes,
        threshold=8
    )

    print_changes(
        "MAY -> JUNE",
        may_june_changes,
        may_june_flagged
    )

    # State persistence
    april_summary = {
        region: {
            "2026-04": months.get("2026-04", 0)
        }
        for region, months in summary.items()
    }

    save_state_v1(
        april_summary,
        STATE_PATH
    )

    loaded_state = load_previous_state_v1(
        STATE_PATH
    )

    print("\n=== STATE PERSISTENCE CHECK ===")
    print("State saved to:", STATE_PATH)
    print("State successfully loaded:", loaded_state == april_summary)

    print("\n=== REQUIRED CHECK ===")
    print(
        "Nellore flagged April->May:",
        "Nellore" in april_may_flagged
    )

    print(
        "Nellore flagged May->June:",
        "Nellore" in may_june_flagged
    )


if __name__ == "__main__":
    main()