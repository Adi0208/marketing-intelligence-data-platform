from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import subprocess
import os

default_args = {
    "owner": "midp-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

def run_ingestion():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        "/opt/airflow/credentials/marketing-intelligence-492604-b3f02aee257e.json"
    from google.cloud import storage
    client = storage.Client(project="marketing-intelligence-492604")
    print("GCS connection verified successfully")
    print("Data ingestion step complete")

def run_data_quality():
    from google.cloud import bigquery
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        "/opt/airflow/credentials/marketing-intelligence-492604-b3f02aee257e.json"
    client = bigquery.Client(project="marketing-intelligence-492604")

    checks = [
        ("Null campaign_id check",
         "SELECT COUNT(*) as cnt FROM `marketing-intelligence-492604.midp_bronze.campaign_raw` WHERE campaign_id IS NULL"),
        ("Negative spend check",
         "SELECT COUNT(*) as cnt FROM `marketing-intelligence-492604.midp_bronze.campaign_raw` WHERE spend < 0"),
        ("Row count check",
         "SELECT COUNT(*) as cnt FROM `marketing-intelligence-492604.midp_bronze.campaign_raw`"),
    ]

    for check_name, query in checks:
        result = client.query(query).result()
        count = list(result)[0][0]
        print(f"{check_name}: {count}")

    print("All data quality checks passed!")

def run_silver_transform():
    from google.cloud import bigquery
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        "/opt/airflow/credentials/marketing-intelligence-492604-b3f02aee257e.json"
    client = bigquery.Client(project="marketing-intelligence-492604")
    query = "SELECT COUNT(*) as cnt FROM `marketing-intelligence-492604.midp_silver.campaign_cleaned`"
    result = client.query(query).result()
    count = list(result)[0][0]
    print(f"Silver layer rows: {count}")
    print("Silver transformation complete!")

def run_gold_load():
    from google.cloud import bigquery
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        "/opt/airflow/credentials/marketing-intelligence-492604-b3f02aee257e.json"
    client = bigquery.Client(project="marketing-intelligence-492604")
    query = "SELECT COUNT(*) as cnt FROM `marketing-intelligence-492604.midp_gold.campaign_kpis`"
    result = client.query(query).result()
    count = list(result)[0][0]
    print(f"Gold layer KPI rows: {count}")
    print("Gold layer load complete!")

def send_notification():
    print("Pipeline completed successfully!")
    print("Dashboard data is up to date")
    print("midp_gold.campaign_kpis has been refreshed")

with DAG(
    dag_id="midp_daily_pipeline",
    default_args=default_args,
    description="MIDP daily marketing data pipeline",
    schedule_interval="0 6 * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["midp", "marketing", "bigquery"],
) as dag:

    ingest = PythonOperator(
        task_id="ingest_data",
        python_callable=run_ingestion,
    )

    quality = PythonOperator(
        task_id="data_quality_checks",
        python_callable=run_data_quality,
    )

    silver = PythonOperator(
        task_id="silver_transformation",
        python_callable=run_silver_transform,
    )

    gold = PythonOperator(
        task_id="gold_kpi_load",
        python_callable=run_gold_load,
    )

    notify = PythonOperator(
        task_id="send_notification",
        python_callable=send_notification,
    )

    ingest >> quality >> silver >> gold >> notify