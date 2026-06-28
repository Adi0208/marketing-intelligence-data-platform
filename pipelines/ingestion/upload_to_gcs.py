import os
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID  = os.getenv("GCP_PROJECT_ID")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

def create_bucket(bucket_name):
    client = storage.Client()
    try:
        bucket = client.get_bucket(bucket_name)
        print(f"Bucket already exists: {bucket_name}")
    except Exception:
        bucket = client.create_bucket(bucket_name, location="US")
        print(f"Bucket created: {bucket_name}")
    return bucket

def upload_file(bucket_name, local_path, gcs_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob   = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
    print(f"  Uploaded: {local_path} → gs://{bucket_name}/{gcs_path}")

if __name__ == "__main__":
    print("Creating GCS bucket...")
    create_bucket(BUCKET_NAME)

    files = {
        "data/raw/campaign_raw.csv": "campaign/campaign_raw.csv",
        "data/raw/email_raw.csv":    "email/email_raw.csv",
        "data/raw/website_raw.csv":  "website/website_raw.csv",
        "data/raw/revenue_raw.csv":  "revenue/revenue_raw.csv",
    }

    print("\nUploading files to GCS...")
    for local_path, gcs_path in files.items():
        upload_file(BUCKET_NAME, local_path, gcs_path)

    print("\nAll files uploaded successfully!")
    print(f"Location: gs://{BUCKET_NAME}/")