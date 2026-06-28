# Marketing Intelligence Data Platform (MIDP)

End-to-end cloud data pipeline for marketing analytics on Google Cloud.

## Architecture

Raw CSV → GCS → BigQuery (Bronze → Silver → Gold) → Looker Studio Dashboard

## Tech Stack

- Python — data generation and pipeline scripts
- Google Cloud Storage — raw data lake
- BigQuery — cloud data warehouse
- Apache Airflow — pipeline orchestration
- Docker — Airflow containerization
- Looker Studio — business intelligence dashboard
- Git and GitHub — version control

## Data Layers

### Bronze — Raw Data
- campaign_raw — campaign details, spend, impressions
- email_raw — email sends, opens, clicks
- website_raw — visits, signups, trial activations
- revenue_raw — revenue and customers acquired

### Silver — Cleaned Data
- Null values handled with COALESCE
- Duplicates removed with ROW_NUMBER
- Text standardized with UPPER and TRIM
- Invalid records flagged

### Gold — Business KPIs
- Open Rate = emails opened / emails sent
- CTR = clicks / emails sent
- Adoption Rate = signups / impressions
- Conversion Rate = trial activations / signups
- ROI = (revenue - spend) / spend
- CPA = spend / customers acquired

## Dashboard Pages

1. Executive Dashboard — impressions, clicks, signups, revenue, ROI
2. Engagement Dashboard — email performance, open rate, CTR by channel
3. Campaign Performance — campaign KPI table and CTR pie chart
4. Funnel and Adoption Analysis — signups and adoption rate by channel
5. Revenue and ROI Analysis — revenue, ROI, top 10 campaigns

## Funnel Results

| Stage | Count |
|-------|-------|
| Emails Sent | 13.6M |
| Emails Opened | 3.0M |
| Clicks | 392K |
| Signups | 69.7K |
| Trial Activations | 23.7K |
| Customers Acquired | 5.7K |
| Revenue | 14.9M |

## Airflow Pipeline

DAG: midp_daily_pipeline runs daily at 6 AM

ingest_data → data_quality_checks → silver_transformation → gold_kpi_load → send_notification

## How to Run

1. Clone the repo
git clone https://github.com/Adi0208/marketing-intelligence-data-platform.git

2. Set up Python environment
python -m venv midp-env
midp-env\Scripts\activate
pip install -r requirements.txt

3. Generate mock data
python data/mock/generate_data.py

4. Upload to GCS
python pipelines/ingestion/upload_to_gcs.py

5. Load BigQuery
python pipelines/transformation/bigquery_setup.py
python pipelines/transformation/create_silver_layer.py
python pipelines/transformation/create_gold_layer.py

6. Start Airflow
cd airflow
docker compose up -d

## Author

Aditya — Data Engineer
GitHub: https://github.com/Adi0208
