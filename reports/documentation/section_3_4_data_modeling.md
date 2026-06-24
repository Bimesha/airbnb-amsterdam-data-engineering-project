# Section 3.4 - Data Modeling

PostgreSQL was selected as the analytical database for this project. The purpose of the data model was to make the cleaned and enriched Airbnb data easier to query for business analysis.

## Modeling Approach

A simple dimensional model was used. This model separates descriptive information into dimension tables and measurable performance information into a fact table.

## Main Tables

| Table | Purpose |
|---|---|
| `dim_host` | Stores host-level information such as host ID, host name, superhost status, and host tenure. |
| `dim_listing` | Stores listing-level descriptive information such as listing ID, room type, property type, capacity, and bedroom count. |
| `dim_neighbourhood` | Stores neighbourhood names and city information. |
| `fact_listing_performance` | Stores measurable fields such as price, availability, estimated occupancy, estimated revenue, review count, and review score. |

## Why This Model Was Used

This structure is simple, explainable, and suitable for analytical SQL queries. It supports questions such as:

- Which room types are most expensive?
- Which neighbourhoods have higher prices or occupancy?
- Which hosts manage the most listings?
- Which listings have higher estimated revenue?
- How do review scores vary by listing type?

## Trade-Offs

The model does not include the full daily calendar table because the calendar file has millions of rows. Instead, the project creates a listing-level calendar summary. This keeps the model smaller and easier to query for the assessment.
