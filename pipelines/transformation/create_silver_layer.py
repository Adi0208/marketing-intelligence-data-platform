import os
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    "C:\\Users\\Asus\\marketing-intelligence-data-platform\\marketing-intelligence-492604-b3f02aee257e.json"

PROJECT_ID = "marketing-intelligence-492604"
client = bigquery.Client(project=PROJECT_ID)

def run_sql_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        sql = f.read()

    # Split by semicolon to run each statement separately
    statements = [s.strip() for s in sql.split(";") if s.strip()]

    for i, statement in enumerate(statements):
        try:
            query_job = client.query(statement)
            query_job.result()
            print(f"  Statement {i+1} executed successfully")
        except Exception as e:
            print(f"  Error in statement {i+1}: {e}")

if __name__ == "__main__":
    print("Creating Silver layer views...")
    run_sql_file("sql/silver/create_silver_views.sql")
    print("\nSilver layer complete!")
    print("Check BigQuery → midp_silver dataset")