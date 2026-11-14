# Project Hope: Data Mining Against the Ebola Outbreak (DRC)

> *"Ihr seid die Hoffnung"*

## Overview
This repository hosts the computational framework and analytical models developed as part of the academic **Data Mining** course. Rather than relying on synthetic or abstract datasets, this course transforms academic theory into a real-world humanitarian mission: tracking, analyzing, and supporting the mitigation of the Ebola (Bundibugyo strain) epidemic in the Democratic Republic of the Congo (DRC).

Working under conditions of infrastructure and logistical challenges in conflict zones, students apply rigorous data science methodologies to open-access data to extract actionable insights for public health surveillance.

---

## Architecture: The Medallion Data Pipeline
To ensure data integrity, reproducibility, and clean collaborative workflows, the project follows a strict **Medallion Architecture**:

* `data/01_bronze_raw/` — **Raw Data Layer:** Immutable, raw data ingested directly from public sources (HDX, WHO RSS feeds, open repositories). Read-only.
* `data/02_silver_cleaned/` — **Cleaned Data Layer:** Processed and standardized datasets (handling missing values, data type coercion, spatial-temporal alignment).
* `data/03_gold_features/` — **Feature & Model Layer:** Aggregated feature matrices, risk scores, anomaly detection results, and predictive model outputs.

---

## Repository Structure

```text
├── data/
│   ├── 01_bronze_raw/       # Raw, versioned data snapshots
│   ├── 02_silver_cleaned/   # Cleaned and standardized data
│   └── 03_gold_features/    # Analytical results and model features
├── workspace/
│   ├── zespol_1_anomalie/   # Student Team 1: Anomaly & Outlier Detection
│   ├── zespol_2_grafy/      # Student Team 2: Network & Graph Analysis
│   └── zespol_3_logistyka/  # Student Team 3: Predictive Modeling & Logistics
└── README.md
