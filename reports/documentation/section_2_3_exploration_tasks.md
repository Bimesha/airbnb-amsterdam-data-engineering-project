# Section 2.3 - Dataset Exploration Tasks

## Selected Dataset

The selected dataset is the Amsterdam Inside Airbnb dataset. Amsterdam was selected as the only city so the project could focus on a clear and complete workflow.

## Files Used

| File | Rows | Columns | Purpose |
|---|---:|---:|---|
| listings.csv.gz | 10,480 | 79 | Main listing, host, price, location, and review score data |
| calendar.csv.gz | 3,825,200 | 7 | Daily availability records for listings |
| reviews.csv.gz | 501,084 | 6 | Review records linked to listings |
| neighbourhoods.csv | 22 | 2 | Neighbourhood reference data |

## Exploration Completed

The following exploration tasks were completed:

- Checked whether all required files were available.
- Recorded file size, row count, and column count.
- Profiled column names, data types, missing values, and sample values.
- Checked duplicate rows.
- Identified main relationships between files.
- Identified key limitations before analysis.

## Main Relationships

- `listings.id` links to `calendar.listing_id`.
- `listings.id` links to `reviews.listing_id`.
- `listings.neighbourhood_cleansed` links to neighbourhood-level grouping.

## Key Observations

The dataset is suitable for a data engineering and analytics workflow. However, calendar price fields were missing, listing prices had missing values, and calendar availability could not confirm actual bookings.
