import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    "C:\\Users\\Asus\\marketing-intelligence-data-platform\\marketing-intelligence-492604-b3f02aee257e.json"

client = bigquery.Client(project=PROJECT_ID)

def create_dataset(dataset_name):
    dataset_id = f"{PROJECT_ID}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    try:
        client.create_dataset(dataset, exists_ok=True)
        print(f"Dataset created: {dataset_name}")
    except Exception as e:
        print(f"Error creating {dataset_name}: {e}")

def load_csv_to_bigquery(gcs_uri, table_id, schema):
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    load_job = client.load_table_from_uri(
        gcs_uri, table_id, job_config=job_config
    )
    load_job.result()
    print(f"  Loaded: {gcs_uri} → {table_id}")

if __name__ == "__main__":

    # Step 1 — Create datasets
    print("Creating BigQuery datasets...")
    create_dataset("midp_bronze")
    create_dataset("midp_silver")
    create_dataset("midp_gold")

    # Step 2 — Define schemas
    campaign_schema = [
        bigquery.SchemaField("campaign_id",   "STRING"),
        bigquery.SchemaField("campaign_name", "STRING"),
        bigquery.SchemaField("channel",       "STRING"),
        bigquery.SchemaField("start_date",    "DATE"),
        bigquery.SchemaField("end_date",      "DATE"),
        bigquery.SchemaField("budget",        "FLOAT64"),
        bigquery.SchemaField("impressions",   "INT64"),
        bigquery.SchemaField("reach",         "INT64"),
        bigquery.SchemaField("spend",         "FLOAT64"),
    ]

    email_schema = [
        bigquery.SchemaField("campaign_id",   "STRING"),
        bigquery.SchemaField("emails_sent",   "INT64"),
        bigquery.SchemaField("emails_opened", "INT64"),
        bigquery.SchemaField("clicks",        "INT64"),
        bigquery.SchemaField("bounced",       "INT64"),
        bigquery.SchemaField("unsubscribed",  "INT64"),
    ]

    website_schema = [
        bigquery.SchemaField("campaign_id",       "STRING"),
        bigquery.SchemaField("website_visits",    "INT64"),
        bigquery.SchemaField("page_views",        "INT64"),
        bigquery.SchemaField("avg_time_on_site",  "FLOAT64"),
        bigquery.SchemaField("signups",           "INT64"),
        bigquery.SchemaField("trial_activations", "INT64"),
    ]

    revenue_schema = [
        bigquery.SchemaField("campaign_id",        "STRING"),
        bigquery.SchemaField("customers_acquired", "INT64"),
        bigquery.SchemaField("revenue",            "FLOAT64"),
        bigquery.SchemaField("avg_deal_size",      "FLOAT64"),
    ]

    # Step 3 — Load CSVs from GCS into Bronze tables
    print("\nLoading data into Bronze layer...")
    BUCKET = "midp-raw-data"

    load_csv_to_bigquery(
        f"gs://{BUCKET}/campaign/campaign_raw.csv",
        f"{PROJECT_ID}.midp_bronze.campaign_raw",
        campaign_schema
    )
    load_csv_to_bigquery(
        f"gs://{BUCKET}/email/email_raw.csv",
        f"{PROJECT_ID}.midp_bronze.email_raw",
        email_schema
    )
    load_csv_to_bigquery(
        f"gs://{BUCKET}/website/website_raw.csv",
        f"{PROJECT_ID}.midp_bronze.website_raw",
        website_schema
    )
    load_csv_to_bigquery(
        f"gs://{BUCKET}/revenue/revenue_raw.csv",
        f"{PROJECT_ID}.midp_bronze.revenue_raw",
        revenue_schema
    )

    print("\nBronze layer setup complete!")
    print(f"Check BigQuery: console.cloud.google.com/bigquery")