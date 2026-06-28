-- ═══════════════════════════════════════════════
-- GOLD LAYER: Business KPIs
-- Project: marketing-intelligence-492604
-- ═══════════════════════════════════════════════

CREATE OR REPLACE TABLE `marketing-intelligence-492604.midp_gold.campaign_kpis` AS
SELECT
  c.campaign_id,
  c.campaign_name,
  c.channel,
  c.budget,
  c.spend,
  c.impressions,
  c.reach,

  -- Email metrics
  e.emails_sent,
  e.emails_opened,
  e.clicks,
  e.bounced,

  -- Website metrics
  w.website_visits,
  w.signups,
  w.trial_activations,

  -- Revenue metrics
  r.customers_acquired,
  r.revenue,
  r.avg_deal_size,

  -- ── KPI CALCULATIONS ──────────────────────────

  -- Email open rate %
  ROUND(SAFE_DIVIDE(e.emails_opened, e.emails_sent) * 100, 2)
    AS open_rate,

  -- Click through rate %
  ROUND(SAFE_DIVIDE(e.clicks, e.emails_sent) * 100, 2)
    AS ctr,

  -- Adoption rate %
  ROUND(SAFE_DIVIDE(w.signups, c.impressions) * 100, 2)
    AS adoption_rate,

  -- Conversion rate %
  ROUND(SAFE_DIVIDE(w.trial_activations, w.signups) * 100, 2)
    AS conversion_rate,

  -- Return on investment %
  ROUND(SAFE_DIVIDE(r.revenue - c.spend, c.spend) * 100, 2)
    AS roi,

  -- Cost per acquisition
  ROUND(SAFE_DIVIDE(c.spend, r.customers_acquired), 2)
    AS cpa,

  -- Revenue per impression
  ROUND(SAFE_DIVIDE(r.revenue, c.impressions), 4)
    AS revenue_per_impression

FROM `marketing-intelligence-492604.midp_silver.campaign_cleaned` c
LEFT JOIN `marketing-intelligence-492604.midp_silver.email_cleaned`   e
  ON c.campaign_id = e.campaign_id
LEFT JOIN `marketing-intelligence-492604.midp_silver.website_cleaned` w
  ON c.campaign_id = w.campaign_id
LEFT JOIN `marketing-intelligence-492604.midp_silver.revenue_cleaned` r
  ON c.campaign_id = r.campaign_id
WHERE c.quality_flag = 'VALID';