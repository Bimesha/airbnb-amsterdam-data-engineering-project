# Airbnb Amsterdam Data Engineering Assessment

## Overview

This project was completed as part of a Data Engineer Intern technical assessment.

I used the Amsterdam Inside Airbnb dataset and built a simple ETL pipeline to practice data engineering concepts such as data ingestion, data cleaning, data transformation, loading data into PostgreSQL, and basic data analysis.

The project also includes exploratory data analysis, a few statistical tests, and a simple machine learning experiment to predict Airbnb prices.


## Selected City

**Amsterdam, North Holland, The Netherlands**

I selected only one city so I could focus on completing the full workflow properly instead of working with multiple datasets.


## Dataset Files

Download the Amsterdam Inside Airbnb dataset and place the following files inside:

```text
data/raw/
```

Required files:

```text
listings.csv.gz
calendar.csv.gz
reviews.csv.gz
neighbourhoods.csv
```

Raw data files are not included in this repository because they are large.

---

## Tools and Libraries

This project was mainly built using:

* Python
* pandas
* PostgreSQL
* SQLAlchemy
* matplotlib
* scipy
* scikit-learn
* Jupyter Notebook
* VS Code
* pgAdmin


## Project Structure

```text
airbnb-data-engineering-project/

├── README.md
├── requirements.txt
├── .env.example
├── .gitignore

├── data/
│   ├── raw/
│   └── processed/

├── scripts/
│   ├── 01_check_files.py
│   ├── 02_profile_data.py
│   ├── 03_extract.py
│   ├── 04_quality_checks.py
│   ├── 05_transform.py
│   ├── 06_enrich_join.py
│   ├── 07_load_to_postgres.py
│   ├── 08_eda_analysis.py
│   ├── 09_statistical_analysis.py
│   ├── 10_price_prediction.py
│   ├── 11_open_innovation.py
│   ├── db_connection.py
│   └── run_pipeline.py

├── sql/
│   └── 03_analysis_queries.sql

├── notebooks/
│   ├── 01_dataset_familiarization.ipynb
│   ├── 02_eda_business_insights.ipynb
│   ├── 03_statistical_analysis.ipynb
│   └── 04_price_prediction.ipynb

├── reports/
│   ├── documentation
│   └── generated_csv

├── figures/
├── demo/
├── architecture/
├── Presentation/
└── exports/
```

---

## Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

---

## PostgreSQL Setup

Create a PostgreSQL database named:

```text
airbnb_db
```

Create a `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=airbnb_db
DB_USER=postgres
DB_PASSWORD=your_password
```


## Running the Project

Run the ETL pipeline:

```bash
python scripts/run_pipeline.py
```

Or run scripts individually:

```bash
python scripts/01_check_files.py
python scripts/02_profile_data.py
python scripts/03_extract.py
python scripts/04_quality_checks.py
python scripts/05_transform.py
python scripts/06_enrich_join.py
python scripts/07_load_to_postgres.py
```

Run analysis scripts:

```bash
python scripts/08_eda_analysis.py
python scripts/09_statistical_analysis.py
python scripts/10_price_prediction.py
python scripts/11_open_innovation.py
```

If PostgreSQL is not available, scripts 01–06 can still be executed.

---

## Notebooks

The notebooks were created mainly for exploring the dataset and presenting results.

```text
01_dataset_familiarization.ipynb
02_eda_business_insights.ipynb
03_statistical_analysis.ipynb
04_price_prediction.ipynb
```

---

## Outputs

Important outputs are saved inside:

```text
reports/
figures/
exports/
```

Some output files include:

```text
validation_summary.csv
cleaning_decision_log.csv
statistical_test_results.csv
price_prediction_results.csv
```

---

## What I Learned

Through this project I practiced:

* Working with compressed CSV datasets
* Data profiling and quality checks
* Cleaning and transforming data using pandas
* Joining multiple datasets
* Loading data into PostgreSQL
* Writing SQL queries for analysis
* Creating visualizations
* Running statistical tests
* Building a simple machine learning model
* Organizing an ETL pipeline into reusable scripts

---

## Limitations

Some limitations of this project:

* Only Amsterdam was analyzed.
* Calendar price information was incomplete, so weekday vs weekend pricing analysis was limited.
* Occupancy and revenue are estimated values.
* Review count was used as an indicator of demand, but not every guest leaves a review.
* Cloud deployment and advanced tools such as Docker or dbt were not included.

---

## AI Usage

I used AI tools for:

* Understanding concepts
* Debugging errors
* Explaining code
* Improving documentation

All code was reviewed, tested, and modified by me during the project.

## Important Note

Raw data files are not included in this archive to keep the submission lightweight. 
To reproduce the project, download the Amsterdam Inside Airbnb files and place them in data/raw/.
