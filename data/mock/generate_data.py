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
        impressions = random.randint(10000, 500000)
        reach       = int(impressions * random.uniform(0.4, 0.8))
        spend       = round(random.uniform(800, 48000), 2)
        budget      = round(spend * random.uniform(1.1, 1.5), 2)
        campaigns.append({
            "campaign_id":   f"C{i:04d}",
            "campaign_name": fake.catch_phrase(),
            "channel":       random.choice(channels),
            "start_date":    start,
            "end_date":      end,
            "budget":        budget,
            "impressions":   impressions,
            "reach":         reach,
            "spend":         spend,
        })
    return pd.DataFrame(campaigns)

def generate_emails(campaign_ids):
    emails = []
    for cid in campaign_ids:
        # Funnel: sent → opened → clicked (each smaller)
        sent      = random.randint(5000, 50000)
        opened    = int(sent    * random.uniform(0.10, 0.35))
        clicked   = int(opened  * random.uniform(0.05, 0.20))
        bounced   = int(sent    * random.uniform(0.01, 0.05))
        unsub     = int(sent    * random.uniform(0.001, 0.01))
        emails.append({
            "campaign_id":   cid,
            "emails_sent":   sent,
            "emails_opened": opened,
            "clicks":        clicked,
            "bounced":       bounced,
            "unsubscribed":  unsub,
        })
    return pd.DataFrame(emails)

def generate_website(campaign_ids, email_df):
    website = []
    for i, cid in enumerate(campaign_ids):
        # Get clicks from email data for this campaign
        email_clicks = int(email_df[email_df["campaign_id"] == cid]["clicks"].values[0])

        # Website visits slightly more than email clicks
        visits = email_clicks + random.randint(100, 2000)

        # Signups MUST be less than visits and less than clicks
        signups = int(visits * random.uniform(0.03, 0.12))

        # Trial activations MUST be less than signups
        trials = int(signups * random.uniform(0.20, 0.50))

        website.append({
            "campaign_id":       cid,
            "website_visits":    visits,
            "page_views":        visits * random.randint(2, 5),
            "avg_time_on_site":  round(random.uniform(1.0, 8.0), 2),
            "signups":           signups,
            "trial_activations": trials,
        })
    return pd.DataFrame(website)

def generate_revenue(campaign_ids, website_df):
    revenue = []
    for cid in campaign_ids:
        # Customers acquired MUST be less than trial activations
        trials = int(website_df[website_df["campaign_id"] == cid]["trial_activations"].values[0])
        customers = int(trials * random.uniform(0.10, 0.40))
        avg_deal  = round(random.uniform(100, 5000), 2)
        rev       = round(customers * avg_deal, 2)
        revenue.append({
            "campaign_id":        cid,
            "customers_acquired": customers,
            "revenue":            rev,
            "avg_deal_size":      avg_deal,
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
    website = generate_website(campaign_ids, emails)
    website.to_csv("data/raw/website_raw.csv", index=False)
    print(f"  website_raw.csv   → {len(website)} rows")

    print("Generating revenue data...")
    revenue = generate_revenue(campaign_ids, website)
    revenue.to_csv("data/raw/revenue_raw.csv", index=False)
    print(f"  revenue_raw.csv   → {len(revenue)} rows")

    print("\nAll files generated successfully!")
    print("\nFunnel Summary:")
    print(f"  Total Emails Sent:    {emails['emails_sent'].sum():,}")
    print(f"  Total Clicks:         {emails['clicks'].sum():,}")
    print(f"  Total Signups:        {website['signups'].sum():,}")
    print(f"  Total Trials:         {website['trial_activations'].sum():,}")
    print(f"  Total Customers:      {revenue['customers_acquired'].sum():,}")
    print(f"  Total Revenue:        ${revenue['revenue'].sum():,.2f}")
