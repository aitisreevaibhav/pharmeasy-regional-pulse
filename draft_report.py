import json
import sqlite3

DB_PATH = "pharmeasy.db"


def draft_report_v1(flagged_regions, metrics):
    """
    Create one Context-Insight-Implication (CII) block
    for every uniquely flagged region.

    flagged_regions can contain regions from either or both
    month transitions.
    """

    unique_regions = list(dict.fromkeys(flagged_regions))
    report = []

    for region in unique_regions:
        region_metrics = metrics.get(region, {})

        april = region_metrics.get("2026-04", 0)
        may = region_metrics.get("2026-05", 0)
        june = region_metrics.get("2026-06", 0)

        april_may = region_metrics.get("April_to_May")
        may_june = region_metrics.get("May_to_June")

        context = (
            f"{region} recorded sales of INR {april:,.2f} in April 2026, "
            f"INR {may:,.2f} in May 2026, and INR {june:,.2f} in June 2026."
        )

        insight_parts = []

        if april_may is not None:
            insight_parts.append(
                f"April-to-May sales changed by {april_may:.2f}%."
            )

        if may_june is not None:
            insight_parts.append(
                f"May-to-June sales changed by {may_june:.2f}%."
            )

        insight = " ".join(insight_parts)

        implication = (
            f"The movement in {region} should be reviewed by the regional "
            f"team against the underlying order and category detail before "
            f"any operational action is taken."
        )

        report.append(
            {
                "region": region,
                "Context": context,
                "Insight": insight,
                "Implication": implication,
            }
        )

    return report


def load_metrics():
    """
    Read region/month sales directly from SQLite and calculate
    the two Month-on-Month percentage changes.
    """

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            region,
            substr(order_date, 1, 7) AS month,
            ROUND(SUM(sales_inr), 2) AS total_sales
        FROM orders_clean
        GROUP BY region, substr(order_date, 1, 7)
        ORDER BY region, month
    """

    rows = conn.execute(query).fetchall()
    conn.close()

    metrics = {}

    for region, month, sales in rows:
        metrics.setdefault(region, {})
        metrics[region][month] = sales

    for region, values in metrics.items():

        april = values.get("2026-04", 0)
        may = values.get("2026-05", 0)
        june = values.get("2026-06", 0)

        if april == 0:
            april_may = 0
        else:
            april_may = ((may - april) / april) * 100

        if may == 0:
            may_june = 0
        else:
            may_june = ((june - may) / may) * 100

        values["April_to_May"] = april_may
        values["May_to_June"] = may_june

    return metrics


def get_flagged_regions(metrics, threshold=8):
    """
    Return the union of regions flagged in either transition.
    """

    flagged = []

    for region, values in metrics.items():

        april_may = values.get("April_to_May", 0)
        may_june = values.get("May_to_June", 0)

        if abs(april_may) > threshold or abs(may_june) > threshold:
            flagged.append(region)

    return flagged


def main():

    metrics = load_metrics()

    flagged_regions = get_flagged_regions(metrics)

    report = draft_report_v1(flagged_regions, metrics)

    print("\n=== CII INSIGHT REPORT ===\n")

    for block in report:
        print(f"Region: {block['region']}")
        print(f"Context: {block['Context']}")
        print(f"Insight: {block['Insight']}")
        print(f"Implication: {block['Implication']}")
        print("-" * 70)

    with open("draft_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\nSaved CII report to draft_report.json")


if __name__ == "__main__":
    main()