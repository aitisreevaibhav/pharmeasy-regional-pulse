import sqlite3
import pandas as pd


DB_PATH = "pharmeasy.db"


def build_database():
    # Load the cleaned order data and region master
    orders = pd.read_csv("orders_clean.csv")
    regions = pd.read_csv("regions_master.csv")

    # Create/connect to SQLite database
    conn = sqlite3.connect(DB_PATH)

    try:
        # Replace tables so the script is repeatable
        regions.to_sql(
            "regions_master",
            conn,
            if_exists="replace",
            index=False
        )

        orders.to_sql(
            "orders_clean",
            conn,
            if_exists="replace",
            index=False
        )

        # Verify row counts
        region_count = conn.execute(
            "SELECT COUNT(*) FROM regions_master"
        ).fetchone()[0]

        order_count = conn.execute(
            "SELECT COUNT(*) FROM orders_clean"
        ).fetchone()[0]

        print(f"regions_master rows: {region_count}")
        print(f"orders_clean rows: {order_count}")
        print(f"Database created: {DB_PATH}")

    finally:
        conn.close()


if __name__ == "__main__":
    build_database()