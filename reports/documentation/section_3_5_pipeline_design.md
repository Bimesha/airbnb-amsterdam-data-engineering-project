# Section 3.5 - Pipeline Design & Automation

The project uses a simple Python-based ETL pipeline. The pipeline is organized into separate scripts so that each step has a clear responsibility.

## Pipeline Steps

| Step | Script | Assessment Section | Purpose |
|---:|---|---|---|
| 1 | `01_check_files.py` | 2.3 / 3.1 | Check required raw files and create file inventory. |
| 2 | `02_profile_data.py` | 2.3 / 3.1 | Profile schemas, data types, missing values, and sample values. |
| 3 | `03_extract.py` | 3.1 | Extract useful columns from raw files. |
| 4 | `04_quality_checks.py` | 3.1 | Run quality checks and identify possible data issues. |
| 5 | `05_transform.py` | 3.2 | Clean and standardize data. |
| 6 | `06_enrich_join.py` | 3.3 | Join datasets and create enriched outputs. |
| 7 | `07_load_to_postgres.py` | 3.4 | Load analytical tables into PostgreSQL. |

## Automation

The `run_pipeline.py` script runs the main ETL steps in order and creates a pipeline log at:

```text
reports/pipeline_run_log.csv
```

The log records the script name, assessment section, status, attempts, start time, end time, duration, and any error message.

## Error Handling

If a step fails, the pipeline stops and records the failure in the pipeline log. This makes the process easier to debug.

## Production Considerations

For a larger production version, the pipeline could be improved with scheduling, Docker, orchestration, database migrations, automated testing, and monitoring. These were not included because, focused on the core workflow.
