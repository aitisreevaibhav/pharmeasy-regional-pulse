# PharmEasy Regional Pulse — Data Quality Report

## Purpose

This report documents the data-quality problems identified in the raw PharmEasy order export and the fixes applied by the cleaning pipeline.

## Data-quality dimensions

| Data-quality dimension | Issue / Fix | Evidence |
|---|---|---|
| Accuracy | Missing `profit_inr` values were imputed using the category-specific mean profit margin calculated from non-missing rows. | 94 missing profit values were imputed. |
| Completeness | Missing `category` values were filled using an exact product-to-category lookup derived from non-missing rows. | 48 missing category values were imputed. |
| Consistency | Region names were stripped of leading/trailing whitespace and title-cased so variants such as `hyderabad`, `HYDERABAD ` and `Hyderabad` map to the same canonical region. | The normalized region values match the active regions in `regions_master.csv`. |
| Timeliness | The pipeline retains the `order_date` field from the monthly export so metrics can be grouped by the April, May and June 2026 reporting periods. | `order_date` is preserved in the cleaned dataset. |
| Validity | The cleaned dataset is checked against the required eight-column schema before it is accepted downstream. | `validate_schema()` returned `validated` for the clean dataset. |
| Uniqueness | Exact duplicate rows were removed before downstream analysis. | Exactly 59 duplicate rows were removed, leaving 2100 rows. |
| Relevance | The cleaning process preserves the fields required for regional order, sales and profit analysis while removing only exact duplicate records and temporary helper fields. | The final dataset contains the eight required analysis columns. |

## Cleaning sequence

The pipeline applies the fixes in this order:

1. Remove exact duplicate rows.
2. Normalize region names.
3. Impute missing categories using the product-to-category lookup.
4. Impute missing profit using category-level mean profit margins.
5. Validate the required schema.
6. Save the cleaned dataset as `orders_clean.csv`.

## Validation results

- Raw dataset: **2159 rows**
- Exact duplicates removed: **59**
- Clean dataset: **2100 rows**
- Missing categories imputed: **48**
- Missing profits imputed: **94**
- Clean schema status: **validated**
- Deliberately broken schema status: **blocked_schema**
- Broken-copy missing column: **`profit_inr`**

## Traceability

Each cleaning action corresponds to a specific data-quality problem rather than an unexplained modification. The cleaning script prints the number of duplicate rows removed and the number of missing category and profit values imputed, and it validates the resulting schema before writing `orders_clean.csv`.