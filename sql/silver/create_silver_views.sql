-- ═══════════════════════════════════════════════
-- SILVER LAYER: Cleaned & Standardized Views
-- Project: marketing-intelligence-492604
-- ═══════════════════════════════════════════════

-- 1. Campaign Cleaned View
CREATE OR REPLACE VIEW `marketing-intelligence-492604.midp_silver.campaign_cleaned` AS
SELECT
  campaign_id,
  UPPER(TRIM(campaign_name))  AS campaign_name,
  UPPER(TRIM(channel))        AS channel,
  start_date,
  end_date,
  COALESCE(budget, 0)         AS budget,
  COALESCE(impressions, 0)    AS impressions,
  COALESCE(reach, 0)          AS reach,
  COALESCE(spend, 0)          AS spend,
  CASE
    WHEN campaign_id IS NULL THEN 'INVALID'
    WHEN spend < 0           THEN 'INVALID'
    WHEN budget < 0          THEN 'INVALID'
    ELSE 'VALID'
  END AS quality_flag
FROM `marketing-intelligence-492604.midp_bronze.campaign_raw`
WHERE campaign_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY campaign_id ORDER BY campaign_id) = 1;

-- 2. Email Cleaned View
CREATE OR REPLACE VIEW `marketing-intelligence-492604.midp_silver.email_cleaned` AS
SELECT
  campaign_id,
  COALESCE(emails_sent,   0)  AS emails_sent,
  COALESCE(emails_opened, 0)  AS emails_opened,
  COALESCE(clicks,        0)  AS clicks,
  COALESCE(bounced,       0)  AS bounced,
  COALESCE(unsubscribed,  0)  AS unsubscribed,
  CASE
    WHEN campaign_id IS NULL  THEN 'INVALID'
    WHEN emails_sent <= 0     THEN 'INVALID'
    ELSE 'VALID'
  END AS quality_flag
FROM `marketing-intelligence-492604.midp_bronze.email_raw`
WHERE campaign_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY campaign_id ORDER BY campaign_id) = 1;

-- 3. Website Cleaned View
CREATE OR REPLACE VIEW `marketing-intelligence-492604.midp_silver.website_cleaned` AS
SELECT
  campaign_id,
  COALESCE(website_visits,    0)    AS website_visits,
  COALESCE(page_views,        0)    AS page_views,
  COALESCE(avg_time_on_site,  0.0)  AS avg_time_on_site,
  COALESCE(signups,           0)    AS signups,
  COALESCE(trial_activations, 0)    AS trial_activations,
  CASE
    WHEN campaign_id IS NULL  THEN 'INVALID'
    WHEN website_visits <= 0  THEN 'INVALID'
    ELSE 'VALID'
  END AS quality_flag
FROM `marketing-intelligence-492604.midp_bronze.website_raw`
WHERE campaign_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY campaign_id ORDER BY campaign_id) = 1;

-- 4. Revenue Cleaned View
CREATE OR REPLACE VIEW `marketing-intelligence-492604.midp_silver.revenue_cleaned` AS
SELECT
  campaign_id,
  COALESCE(customers_acquired, 0)    AS customers_acquired,
  COALESCE(revenue,            0.0)  AS revenue,
  COALESCE(avg_deal_size,      0.0)  AS avg_deal_size,
  CASE
    WHEN campaign_id IS NULL  THEN 'INVALID'
    WHEN revenue < 0          THEN 'INVALID'
    ELSE 'VALID'
  END AS quality_flag
FROM `marketing-intelligence-492604.midp_bronze.revenue_raw`
WHERE campaign_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY campaign_id ORDER BY campaign_id) = 1;