# Section 8 - Open Innovation Challenge

A small rule-based market opportunity finder was created as the open innovation component of this project.

## Objective

The objective was to turn the cleaned and enriched dataset into simple business-facing outputs that could support Airbnb market understanding.

## Outputs Created

| Output File | Purpose |
|---|---|
| `exports/value_neighbourhoods.csv` | Identifies neighbourhoods with lower prices and good ratings. |
| `exports/premium_neighbourhoods.csv` | Identifies higher-priced neighbourhoods. |
| `exports/high_occupancy_neighbourhoods.csv` | Identifies neighbourhoods with higher estimated occupancy. |
| `exports/improvement_opportunities.csv` | Identifies listings with many reviews but lower ratings. |
| `exports/top_estimated_revenue_listings.csv` | Identifies listings with high estimated revenue. |

## Method

The feature uses simple rule-based filtering instead of a complex machine learning model. This makes the output easy to explain.

## Business Value

The output can help identify:

- affordable but well-rated areas,
- premium neighbourhoods,
- high-demand areas,
- listings that may need quality improvement,
- and listings with strong estimated revenue potential.

## Limitation

The results depend on estimated occupancy and listing-level price, so they should be treated as directional insights rather than exact business truth.
