import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()
random.seed(42)

def generate_campaigns(n=500):
    channels = ["Email", "Website", "Events", "Digital Ads"]
    campaigns = []
    for i in range(1, n + 1):
        start = fake.date_between(start_date="-12M", end_date="-1M")
        end   = start + timedelta(days=random.randint(7, 60))
        campaigns.append({
            "campaign_id":   f"C{i:04d}",
            "campaign_name": fake.catch_phrase(),
            "channel":       random.choice(channels),
            "start_date":    start,
            "end_date":      end,
            "budget":        round(random.uniform(1000, 50000), 2),
            "impressions":   random.randint(10000, 500000),
            "reach":         random.randint(5000,  200000),
            "spend":         round(random.uniform(800, 48000), 2),
        })
    return pd.DataFrame(campaigns)

def generate_emails(campaign_ids):
    emails = []
    for cid in campaign_ids:
        sent    = random.randint(1000, 50000)
        opened  = int(sent  * random.uniform(0.10, 0.40))
        clicked = int(opened * random.uniform(0.05, 0.25))
        emails.append({
            "campaign_id":    cid,
            "emails_sent":    sent,
            "emails_opened":  opened,
            "clicks":         clicked,
            "bounced":        int(sent * random.uniform(0.01, 0.05)),
            "unsubscribed":   int(sent * random.uniform(0.001, 0.01)),
        })
    return pd.DataFrame(emails)

def generate_website(campaign_ids):
    website = []
    for cid in campaign_ids:
        visits  = random.randint(500, 20000)
        signups = int(visits * random.uniform(0.05, 0.20))
        website.append({
            "campaign_id":       cid,
            "website_visits":    visits,
            "page_views":        visits * random.randint(2, 6),
            "avg_time_on_site":  round(random.uniform(1.0, 8.0), 2),
            "signups":           signups,
            "trial_activations": int(signups * random.uniform(0.30, 0.70)),
        })
    return pd.DataFrame(website)

def generate_revenue(campaign_ids):
    revenue = []
    for cid in campaign_ids:
        revenue.append({
            "campaign_id":        cid,
            "customers_acquired": random.randint(10, 500),
            "revenue":            round(random.uniform(5000, 200000), 2),
            "avg_deal_size":      round(random.uniform(100, 5000), 2),
        })
    return pd.DataFrame(revenue)

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)

    print("Generating campaign data...")
    campaigns = generate_campaigns(500)
    campaigns.to_csv("data/raw/campaign_raw.csv", index=False)
    print(f"  campaign_raw.csv  → {len(campaigns)} rows")

    campaign_ids = campaigns["campaign_id"].tolist()

    print("Generating email data...")
    emails = generate_emails(campaign_ids)
    emails.to_csv("data/raw/email_raw.csv", index=False)
    print(f"  email_raw.csv     → {len(emails)} rows")

    print("Generating website data...")
    website = generate_website(campaign_ids)
    website.to_csv("data/raw/website_raw.csv", index=False)
    print(f"  website_raw.csv   → {len(website)} rows")

    print("Generating revenue data...")
    revenue = generate_revenue(campaign_ids)
    revenue.to_csv("data/raw/revenue_raw.csv", index=False)
    print(f"  revenue_raw.csv   → {len(revenue)} rows")

    print("\nAll files generated successfully!")
    print("Location: data/raw/")