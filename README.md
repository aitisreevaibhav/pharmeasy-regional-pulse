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