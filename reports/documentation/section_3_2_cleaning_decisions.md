# Section 3.2 - Data Cleaning & Standardization

The cleaning and standardization step is implemented in `scripts/05_transform.py`.

## Cleaning Completed

| Requirement | Implementation |
|---|---|
| Standardize price columns | Removed `$` symbols and commas, then converted price to numeric as `price_clean`. |
| Parse date fields | Converted `host_since`, calendar `date`, and review `date` to datetime format. |
| Normalize free-text fields | Trimmed spaces and cleaned repeated whitespace in names, property types, room types, and neighbourhood names. |
| Handle missing values | Filled missing listing and host names with `Unknown`; filled review count and review frequency with `0`; kept missing review scores as null. |
| Remove or flag invalid records | Created validation flags for missing prices, invalid prices, missing review scores, invalid coordinates, invalid calendar dates, invalid availability values, and invalid review dates. |
| Standardize geography | Added city name as `Amsterdam` and rounded latitude/longitude to five decimal places. |

## Output Files

- `data/processed/clean_listings.csv`
- `data/processed/clean_calendar.csv`
- `data/processed/clean_reviews.csv`
- `data/processed/clean_neighbourhoods.csv`
- `reports/cleaning_summary.csv`
- `reports/validation_summary.csv`
- `reports/cleaning_decision_log.csv`

## Decision

Invalid or suspicious records were flagged rather than removed. This keeps the dataset traceable and allows later analysis steps to decide whether to filter specific records.
