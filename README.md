# PharmEasy Regional Pulse

## Project Overview

Guntur sales increased by **122.19% from April to May 2026**, then decreased by **28.11% from May to June 2026**. The project builds a complete regional sales analysis pipeline from raw data to a Streamlit dashboard and review workflow.

## Setup and Run

Run the following commands in order:

```bash
pip install pandas numpy streamlit plotly
python generate_dataset.py
python clean_data.py
python build_db.py
python queries.py
python metrics_engine.py
python draft_report.py
python review_gate.py
streamlit run app.py                         

## 4-Artifact Cover Note

### 1. Dashboard

Run `app.py` to open the interactive Streamlit dashboard with overview KPIs, category analysis, regional comparison, monthly trends, and region-month detail.

### 2. Embedded CII Narrative

The dashboard contains an executive summary using a Context, Insight, and Implication structure.

### 3. Recommendation Memo

See `memo.md` for the Guntur recommendation memo, including evidence, recommendation, next check, and assumptions.

### 4. Presentation Storyline

See `presentation_storyline.md` for the Executive SCR storyline, Regional Manager OCD storyline, and anticipated pushback questions.

## Reviewer Consumption Order

1. Run the pipeline using the commands above.
2. Open the Streamlit dashboard using `streamlit run app.py`.
3. Read the embedded executive summary.
4. Read `memo.md`.
5. Read `presentation_storyline.md`.
6. Review `data_quality_report.md`, `reliability_checklist.md`, and `audit_log.jsonl`.

## Unverified Assumption

The data does not show the exact reason for the Guntur sales increase in May 2026.   