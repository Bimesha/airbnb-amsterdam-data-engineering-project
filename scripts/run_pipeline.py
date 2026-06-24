from pathlib import Path
from datetime import datetime
import subprocess
import sys
import pandas as pd


# Folder setup
reports_folder = Path("reports/generated_csv")
reports_folder.mkdir(parents=True, exist_ok=True)


# Pipeline steps
pipeline_steps = [
    {
        "step_no": 1,
        "section": "2.3 / 3.1",
        "script": "scripts/01_check_files.py",
        "description": "Check downloaded raw files"
    },
    {
        "step_no": 2,
        "section": "2.3 / 3.1",
        "script": "scripts/02_profile_data.py",
        "description": "Profile datasets and create schema reports"
    },
    {
        "step_no": 3,
        "section": "3.1",
        "script": "scripts/03_extract.py",
        "description": "Extract useful columns from raw files"
    },
    {
        "step_no": 4,
        "section": "3.1",
        "script": "scripts/04_quality_checks.py",
        "description": "Run data quality checks"
    },
    {
        "step_no": 5,
        "section": "3.2",
        "script": "scripts/05_transform.py",
        "description": "Clean and standardize data"
    },
    {
        "step_no": 6,
        "section": "3.3",
        "script": "scripts/06_enrich_join.py",
        "description": "Join and enrich datasets"
    },
    {
        "step_no": 7,
        "section": "3.4",
        "script": "scripts/07_load_to_postgres.py",
        "description": "Load data model into PostgreSQL"
    }
]


# Run pipeline
pipeline_log = []
max_attempts = 2

print("\nStarting Airbnb Amsterdam ETL Pipeline")
print("=" * 60)

for step in pipeline_steps:
    step_no = step["step_no"]
    section = step["section"]
    script = step["script"]
    description = step["description"]

    print(f"\nStep {step_no}: {description}")
    print(f"Script: {script}")

    start_time = datetime.now()
    status = "failed"
    error_message = ""

    script_path = Path(script)

    if not script_path.exists():
        end_time = datetime.now()

        error_message = f"Script not found: {script}"

        pipeline_log.append({
            "step_no": step_no,
            "section": section,
            "script": script,
            "description": description,
            "status": status,
            "attempts": 0,
            "start_time": start_time,
            "end_time": end_time,
            "duration_seconds": round((end_time - start_time).total_seconds(), 2),
            "error_message": error_message
        })

        print(error_message)
        break

    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}...")

        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            status = "success"
            error_message = ""
            print("Success")
            break
        else:
            error_message = result.stderr
            print("Failed")

    end_time = datetime.now()

    pipeline_log.append({
        "step_no": step_no,
        "section": section,
        "script": script,
        "description": description,
        "status": status,
        "attempts": attempt,
        "start_time": start_time,
        "end_time": end_time,
        "duration_seconds": round((end_time - start_time).total_seconds(), 2),
        "error_message": error_message
    })

    if status == "failed":
        print("\nPipeline stopped because a step failed.")
        print(f"Failed script: {script}")
        print("Check the error message in reports/generated_csv/pipeline_run_log.csv")
        break


# Save pipeline log
pipeline_log_df = pd.DataFrame(pipeline_log)

pipeline_log_df.to_csv(
    reports_folder / "pipeline_run_log.csv",
    index=False
)

# Final message
if len(pipeline_log_df) == len(pipeline_steps) and all(pipeline_log_df["status"] == "success"):
    print("\nPipeline completed successfully.")
else:
    print("\nPipeline did not complete fully.")

print("\nPipeline log saved:")
print("reports/generated_csv/pipeline_run_log.csv")