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

Workflow & Environment (Google Colab + GitHub)

To accommodate restricted laboratory environments without local administrative privileges, all computational work is executed via Google Colab in the browser.
1. Reading Data into Colab

Students can seamlessly ingest the latest data directly into their notebooks without local Git installation:

```python
import pandas as pd

url = "[https://raw.githubusercontent.com/sggw-wzim/projekt-nadzieja-ebola/main/data/01_bronze_raw/your_data_file.csv](https://raw.githubusercontent.com/sggw-wzim/projekt-nadzieja-ebola/main/data/01_bronze_raw/your_data_file.csv)"
df = pd.read_csv(url)
print(df.head())

2. Saving Work

    Notebooks (.ipynb): Saved directly back to the student team's designated workspace folder via Colab's GitHub integration (File -> Save a copy in GitHub).

    Artifacts/Results (CSV): Uploaded manually via the GitHub web interface into the respective workspace or gold layer.

Data Sources

The project aggregates public, open-source data from verified international bodies:

    UN OCHA Humanitarian Data Exchange (HDX): Geographic boundaries, conflict zones, and baseline humanitarian datasets.

    World Health Organization (WHO) / Africa CDC: Disease outbreak news, surveillance reports, and epidemiological updates.

Open Science & Mission Impact

In alignment with Open Science principles, all cleaned datasets, analytical pipelines, and visualization notebooks are published openly. At the conclusion of the academic cycle, synthesized technical summaries and risk models are designed to be shared with humanitarian actors operating in the field.
