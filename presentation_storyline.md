# Presentation Storyline

## 1. Executive — Situation / Complication / Resolution

### Situation

Guntur's cleaned April→May sales increased by **122.19%**. [HIGH]

Guntur sales were **INR 62,442.27 in April** and **INR 138,738.93 in May**. [HIGH]

### Complication

The pipeline uses an **8% operational alert threshold**. [LOW]

The 122.19% movement shows that sales changed sharply, but the percentage alone does not prove why the change happened. [MEDIUM]

### Resolution

Use the dashboard to review Guntur's category and monthly detail before taking operational action. [MEDIUM]

The next monthly export should be processed through the same pipeline to check whether the movement continues. [MEDIUM]


## 2. Regional Manager — Overview / Category / Detail

### Overview

Guntur's April→May sales change is **+122.19%**. [HIGH]

The number of Guntur orders increased from **51 in April to 77 in May**. [HIGH]

### Category

In May, **Wellness & Nutrition** had the highest Guntur sales at **INR 53,085.01**. [HIGH]

The dashboard can be used to compare all six categories and check whether the category mix supports the overall sales movement. [MEDIUM]

### Detail

The region-month table shows:

- April sales: **INR 62,442.27** [HIGH]
- May sales: **INR 138,738.93** [HIGH]
- June sales: **INR 99,745.18** [HIGH]

May→June then decreased by **28.11%**. [HIGH]

The detail view helps check whether the April→May increase continued or reversed.


## Anticipated Pushback Q&A

### Q1 — Why should I believe this number?

1. **Acknowledge:** It is reasonable to question a large month-on-month movement.
2. **Verified vs. unverified:** The +122.19% figure is calculated from the cleaned dataset using the SQL region-by-month sales aggregation. The reason for the increase is not verified.
3. **Resolution and timing:** Review the category and order detail now, then process the next monthly export using the same pipeline.


### Q2 — What if another explanation caused the increase?

1. **Acknowledge:** A percentage change alone cannot identify the cause.
2. **Verified vs. unverified:** The pipeline verifies the sales movement and provides category and monthly detail, but it does not prove a causal explanation.
3. **Resolution and timing:** Review the current Guntur detail and check the next monthly export during the next monthly review cycle.