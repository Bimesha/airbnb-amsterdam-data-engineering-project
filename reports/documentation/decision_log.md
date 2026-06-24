# Decision Log

This document records the main project decisions made during the Airbnb Amsterdam data engineering assessment.

| No. | Area | Decision | Reason |
|---:|---|---|---|
| 1 | City selection | Analyze Amsterdam only | The assessment scope was broad, so one city allowed better profiling, cleaning, modeling, and explanation within the available time. |
| 2 | Dataset files | Use listings, calendar, reviews, and neighbourhoods | These four files cover listings, availability, reviews, and geographic grouping. |
| 3 | Pipeline design | Use a simple ETL pipeline | The source data is CSV-based, so Python ETL is easy to reproduce and explain. |
| 4 | Processing tool | Use Python and pandas | pandas is suitable for CSV reading, cleaning, joining, and summary creation. |
| 5 | Database | Use PostgreSQL | PostgreSQL demonstrates relational modeling and SQL analysis skills. |
| 6 | Data model | Build simple dimension and fact tables | A star-style model is easy to query and appropriate for analytical reporting. |
| 7 | Price cleaning | Remove currency symbols and commas, then cast to numeric | Price is required for EDA, statistics, and price prediction. |
| 8 | Missing listing prices | Keep missing prices as null | Creating artificial price values could distort price analysis. |
| 9 | Calendar prices | Do not use calendar price fields | Calendar `price` and `adjusted_price` fields were missing, so daily price analysis was not reliable. |
| 10 | Occupancy | Estimate occupancy from calendar availability | Actual bookings were not available, so calendar availability was used only as a proxy. |
| 11 | Revenue | Calculate estimated revenue only | Revenue is approximate because occupancy is estimated and listing-level price is used. |
| 12 | Review data | Use review count as a demand proxy | Reviews are useful but not equal to total bookings because not every guest leaves a review. |
| 13 | Missing review scores | Keep missing rating values as null | Filling missing ratings could create misleading average scores. |
| 14 | Validation issues | Flag invalid records instead of deleting them | Flagging keeps the data traceable and avoids unnecessary data loss. |
| 15 | Machine learning | Use simple Linear Regression and Random Forest models | The goal was to demonstrate a basic price prediction experiment, not build a production model. |
| 16 | Notebooks | Use notebooks as supporting explanation only | Scripts remain the main pipeline; notebooks summarize outputs for review. |
| 17 | Advanced tools | Exclude cloud, Docker, dbt, and dashboards | Priority was given to completing the core data engineering and analysis workflow clearly. |
