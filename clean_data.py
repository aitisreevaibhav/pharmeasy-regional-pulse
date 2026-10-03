import pandas as pd


REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "region",
    "category",
    "product",
    "quantity",
    "sales_inr",
    "profit_inr",
]


def validate_schema(df, required_columns):
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    return {
        "status": "validated" if not missing_columns else "blocked_schema",
        "row_count": len(df),
        "missing_columns": missing_columns,
    }


def clean_data(
    raw_path="pharmeasy_orders_raw.csv",
    regions_path="regions_master.csv",
    output_path="orders_clean.csv",
):
    # Load raw data
    df = pd.read_csv(raw_path)

    original_rows = len(df)

    # 1. Remove exact duplicate rows
    before_dedup = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before_dedup - len(df)

    print(f"Exact duplicate rows removed: {duplicates_removed}")

    # 2. Normalize region names
    df["region"] = (
        df["region"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    regions_master = pd.read_csv(regions_path)

    active_regions = set(regions_master["region"]) - {"Kurnool"}

    invalid_regions = sorted(
        set(df["region"]) - active_regions
    )

    if invalid_regions:
        raise ValueError(
            f"Unexpected region names after normalization: {invalid_regions}"
        )

    # 3. Impute missing category using product → category lookup
    product_category_lookup = (
        df.dropna(subset=["category"])
        .drop_duplicates(subset=["product"])
        .set_index("product")["category"]
        .to_dict()
    )

    missing_category_before = df["category"].isna().sum()

    df["category"] = df["category"].fillna(
        df["product"].map(product_category_lookup)
    )

    missing_category_after = df["category"].isna().sum()

    if missing_category_after > 0:
        raise ValueError(
            "Some category values could not be imputed."
        )

    print(
        f"Missing category values imputed: "
        f"{missing_category_before}"
    )

    # 4. Impute missing profit using category mean margin
    df["sales_inr"] = pd.to_numeric(
        df["sales_inr"],
        errors="coerce"
    )

    df["profit_inr"] = pd.to_numeric(
        df["profit_inr"],
        errors="coerce"
    )

    df["profit_margin"] = (
        df["profit_inr"] / df["sales_inr"]
    )

    category_mean_margin = (
        df.dropna(subset=["profit_margin"])
        .groupby("category")["profit_margin"]
        .mean()
        .to_dict()
    )

    missing_profit_before = df["profit_inr"].isna().sum()

    missing_profit_mask = df["profit_inr"].isna()

    df.loc[missing_profit_mask, "profit_inr"] = (
        df.loc[missing_profit_mask, "sales_inr"]
        * df.loc[missing_profit_mask, "category"]
        .map(category_mean_margin)
    ).round(2)

    missing_profit_after = df["profit_inr"].isna()

    if missing_profit_after.sum() > 0:
        raise ValueError(
            "Some profit values could not be imputed."
        )

    print(
        f"Missing profit values imputed: "
        f"{missing_profit_before}"
    )

    # Remove helper column
    df = df.drop(columns=["profit_margin"])

    # 5. Validate cleaned dataset
    validation = validate_schema(
        df,
        REQUIRED_COLUMNS
    )

    print("Clean-data schema validation:")
    print(validation)

    if validation["status"] != "validated":
        raise ValueError(
            "Clean dataset failed schema validation."
        )

    # Save clean dataset
    df.to_csv(output_path, index=False)

    print(f"Original raw rows: {original_rows}")
    print(f"Clean rows: {len(df)}")
    print(f"Saved clean dataset to: {output_path}")

    return df


if __name__ == "__main__":
    clean_df = clean_data()

    # Deliberately broken copy to demonstrate blocked_schema
    broken_df = clean_df.drop(columns=["profit_inr"])

    broken_validation = validate_schema(
        broken_df,
        REQUIRED_COLUMNS
    )

    print("Broken-copy schema validation:")
    print(broken_validation)