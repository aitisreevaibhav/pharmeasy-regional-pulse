import sqlite3

DB_PATH = "pharmeasy.db"


def run_query(conn, sql):
    cursor = conn.execute(sql)
    return cursor.fetchall()


def main():
    conn = sqlite3.connect(DB_PATH)

    # ---------------------------------------------------------
    # 1. LEFT JOIN vs INNER JOIN row counts
    # ---------------------------------------------------------
    print("\n=== 1. ROW COUNT CHECK ===")

    left_count = run_query(
        conn,
        """
        SELECT COUNT(*)
        FROM regions_master r
        LEFT JOIN orders_clean o
        ON r.region = o.region;
        """
    )[0][0]

    inner_count = run_query(
        conn,
        """
        SELECT COUNT(*)
        FROM regions_master r
        INNER JOIN orders_clean o
        ON r.region = o.region;
        """
    )[0][0]

    print(f"LEFT JOIN row count: {left_count}")
    print(f"INNER JOIN row count: {inner_count}")
    print(f"Difference: {left_count - inner_count}")


    # ---------------------------------------------------------
    # 2. Duplicate order_id check
    # ---------------------------------------------------------
    print("\n=== 2. DUPLICATE ORDER_ID CHECK ===")

    duplicates = run_query(
        conn,
        """
        SELECT order_id, COUNT(*) AS duplicate_count
        FROM orders_clean
        GROUP BY order_id
        HAVING COUNT(*) > 1;
        """
    )

    if len(duplicates) == 0:
        print("No duplicate order_id values found.")
    else:
        for row in duplicates:
            print(row)


    # ---------------------------------------------------------
    # 3. COUNT(*) vs COUNT(order_id)
    # ---------------------------------------------------------
    print("\n=== 3. COUNT(*) VS COUNT(order_id) ===")

    comparison = run_query(
        conn,
        """
        SELECT
            r.region,
            COUNT(*) AS count_star,
            COUNT(o.order_id) AS count_order_id
        FROM regions_master r
        LEFT JOIN orders_clean o
        ON r.region = o.region
        GROUP BY r.region
        ORDER BY r.region;
        """
    )

    print("Region | COUNT(*) | COUNT(order_id)")
    print("-----------------------------------")

    for region, count_star, count_order_id in comparison:
        print(
            f"{region} | {count_star} | {count_order_id}"
        )


    # Show where the two counts disagree
    print("\nRegions where COUNT(*) and COUNT(order_id) disagree:")

    for region, count_star, count_order_id in comparison:
        if count_star != count_order_id:
            print(
                f"{region}: "
                f"COUNT(*)={count_star}, "
                f"COUNT(order_id)={count_order_id}"
            )


    # ---------------------------------------------------------
    # 4. Per-region order counts
    # ---------------------------------------------------------
    print("\n=== 4. PER-REGION ORDER COUNTS ===")

    region_counts = run_query(
        conn,
        """
        SELECT
            r.region,
            COUNT(o.order_id) AS order_count
        FROM regions_master r
        LEFT JOIN orders_clean o
        ON r.region = o.region
        GROUP BY r.region
        ORDER BY order_count ASC;
        """
    )

    for region, order_count in region_counts:
        print(f"{region}: {order_count}")


    # ---------------------------------------------------------
    # 5. Region × Month sales
    # ---------------------------------------------------------
    print("\n=== 5. REGION × MONTH SALES ===")

    monthly_sales = run_query(
        conn,
        """
        SELECT
            region,
            substr(order_date, 1, 7) AS month,
            ROUND(SUM(sales_inr), 2) AS total_sales_inr
        FROM orders_clean
        GROUP BY region, month
        ORDER BY region, month;
        """
    )

    print("Region | Month | Sales (INR)")
    print("---------------------------")

    for region, month, sales in monthly_sales:
        print(f"{region} | {month} | {sales}")


    conn.close()


if __name__ == "__main__":
    main()