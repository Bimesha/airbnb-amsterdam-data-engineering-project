from pathlib import Path
import pandas as pd

# Define folders
processed_folder = Path("data/processed")
reports_folder = Path("reports/generated_csv")
reports_folder.mkdir(parents=True, exist_ok=True)

print("Starting transform step...\n")


# Helper functions
def clean_text(series):
    """
    Clean text values by:
    1. Converting values to pandas string type
    2. Removing leading and trailing spaces
    3. Replacing multiple spaces with one space
    """
    return (
        series
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )


# Read extracted files

listings = pd.read_csv(
    processed_folder / "extracted_listings.csv",
    low_memory=False
)

calendar = pd.read_csv(
    processed_folder / "extracted_calendar.csv",
    low_memory=False
)

reviews = pd.read_csv(
    processed_folder / "extracted_reviews.csv",
    low_memory=False
)

neighbourhoods = pd.read_csv(
    processed_folder / "extracted_neighbourhoods.csv",
    low_memory=False
)


# Clean listings table
# Rename id column to listing_id for clearer table relationships
listings = listings.rename(columns={"id": "listing_id"})

# Add selected city name
listings["city"] = "Amsterdam"

# Clean price column by removing currency symbols, commas, and extra spaces
listings["price_clean"] = (
    listings["price"]
    .astype("string")
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

# Convert cleaned price values into numeric format
listings["price_clean"] = pd.to_numeric(
    listings["price_clean"],
    errors="coerce"
)

# Flag missing price records
listings["missing_price_flag"] = (
    listings["price_clean"].isna()
)

# Flag invalid price records where price is zero or negative
listings["invalid_price_flag"] = (
    listings["price_clean"].notna()
    &
    (listings["price_clean"] <= 0)
)

# Convert host_since column into datetime format
listings["host_since"] = pd.to_datetime(
    listings["host_since"],
    errors="coerce"
)

# Flag missing or invalid host_since values
listings["invalid_host_since_flag"] = (
    listings["host_since"].isna()
)

# Clean important text and category fields
listings["name"] = (
    clean_text(listings["name"])
    .fillna("Unknown")
)

listings["host_name"] = (
    clean_text(listings["host_name"])
    .fillna("Unknown")
)

listings["room_type"] = (
    clean_text(listings["room_type"])
    .fillna("Unknown")
)

listings["property_type"] = (
    clean_text(listings["property_type"])
    .fillna("Unknown")
)

listings["neighbourhood_cleansed"] = (
    clean_text(
        listings["neighbourhood_cleansed"]
    )
    .fillna("Unknown")
)

# Define accepted room type values
room_type_map = {
    "Entire home/apt": "Entire home/apt",
    "Private room": "Private room",
    "Shared room": "Shared room",
    "Hotel room": "Hotel room"
}

# Standardize room type values
listings["room_type"] = (
    listings["room_type"]
    .replace(room_type_map)
)

# Convert host_is_superhost from t/f into True/False if column exists
if "host_is_superhost" in listings.columns:

    listings["host_is_superhost"] = (
        listings["host_is_superhost"]
        .map({
            "t": True,
            "f": False
        })
    )

# Convert instant_bookable from t/f into True/False if column exists
if "instant_bookable" in listings.columns:

    listings["instant_bookable"] = (
        listings["instant_bookable"]
        .map({
            "t": True,
            "f": False
        })
    )

# Define columns that should be numeric
numeric_columns = [
    "accommodates",
    "bedrooms",
    "beds",
    "minimum_nights",
    "maximum_nights",
    "availability_365",
    "number_of_reviews",
    "review_scores_rating",
    "reviews_per_month"
]

# Convert selected columns into numeric format
for column in numeric_columns:

    if column in listings.columns:

        listings[column] = pd.to_numeric(
            listings[column],
            errors="coerce"
        )

# Fill missing review count fields with 0
listings["number_of_reviews"] = (
    listings["number_of_reviews"]
    .fillna(0)
)

listings["reviews_per_month"] = (
    listings["reviews_per_month"]
    .fillna(0)
)

# Flag missing review score values instead of replacing them
listings["missing_review_score_flag"] = (
    listings["review_scores_rating"]
    .isna()
)

# Convert latitude and longitude into numeric values and round them
listings["latitude"] = (
    pd.to_numeric(
        listings["latitude"],
        errors="coerce"
    )
    .round(5)
)

listings["longitude"] = (
    pd.to_numeric(
        listings["longitude"],
        errors="coerce"
    )
    .round(5)
)

# Flag missing or invalid coordinate values
listings["invalid_coordinate_flag"] = (

    listings["latitude"].isna()

    |

    listings["longitude"].isna()

    |

    (listings["latitude"] < -90)

    |

    (listings["latitude"] > 90)

    |

    (listings["longitude"] < -180)

    |

    (listings["longitude"] > 180)
)


# Clean calendar table
# Convert calendar date into datetime format
calendar["date"] = pd.to_datetime(
    calendar["date"],
    errors="coerce"
)

# Flag missing or invalid calendar dates
calendar["invalid_calendar_date_flag"] = (
    calendar["date"].isna()
)

# Convert available column from t/f into True/False
calendar["is_available"] = (
    calendar["available"]
    .map({
        "t": True,
        "f": False
    })
)

# Flag invalid available values
calendar["invalid_available_flag"] = (
    calendar["is_available"]
    .isna()
)


# Clean reviews table
# Rename review id column
reviews = reviews.rename(
    columns={"id": "review_id"}
)

# Convert review date into datetime format
reviews["date"] = pd.to_datetime(
    reviews["date"],
    errors="coerce"
)

# Flag missing or invalid review dates
reviews["invalid_review_date_flag"] = (
    reviews["date"].isna()
)


# Clean neighbourhoods table
# Add selected city name
neighbourhoods["city"] = "Amsterdam"

# Clean neighbourhood names
neighbourhoods["neighbourhood"] = (
    clean_text(
        neighbourhoods["neighbourhood"]
    )
    .fillna("Unknown")
)


# Save cleaned data
listings.to_csv(
    processed_folder / "clean_listings.csv",
    index=False
)

calendar.to_csv(
    processed_folder / "clean_calendar.csv",
    index=False
)

reviews.to_csv(
    processed_folder / "clean_reviews.csv",
    index=False
)

neighbourhoods.to_csv(
    processed_folder / "clean_neighbourhoods.csv",
    index=False
)


# Create summary report
summary = [

    {
        "table": "clean_listings",
        "rows": len(listings),
        "columns": len(listings.columns)
    },

    {
        "table": "clean_calendar",
        "rows": len(calendar),
        "columns": len(calendar.columns)
    },

    {
        "table": "clean_reviews",
        "rows": len(reviews),
        "columns": len(reviews.columns)
    },

    {
        "table": "clean_neighbourhoods",
        "rows": len(neighbourhoods),
        "columns": len(neighbourhoods.columns)
    }

]

pd.DataFrame(summary).to_csv(
    reports_folder / "cleaning_summary.csv",
    index=False
)


# Create validation report
validation_summary = [

    {
        "check": "missing_price",
        "table": "listings",
        "flagged_records": int(
            listings["missing_price_flag"].sum()
        )
    },

    {
        "check": "invalid_price",
        "table": "listings",
        "flagged_records": int(
            listings["invalid_price_flag"].sum()
        )
    },

    {
        "check": "missing_review_score",
        "table": "listings",
        "flagged_records": int(
            listings["missing_review_score_flag"].sum()
        )
    },

    {
        "check": "invalid_coordinates",
        "table": "listings",
        "flagged_records": int(
            listings["invalid_coordinate_flag"].sum()
        )
    },

    {
        "check": "invalid_calendar_date",
        "table": "calendar",
        "flagged_records": int(
            calendar["invalid_calendar_date_flag"].sum()
        )
    },

    {
        "check": "invalid_available_value",
        "table": "calendar",
        "flagged_records": int(
            calendar["invalid_available_flag"].sum()
        )
    },

    {
        "check": "invalid_review_date",
        "table": "reviews",
        "flagged_records": int(
            reviews["invalid_review_date_flag"].sum()
        )
    }

]

pd.DataFrame(validation_summary).to_csv(
    reports_folder / "validation_summary.csv",
    index=False
)


# Create cleaning decision log
cleaning_decisions = [

    {
        "area": "price",
        "decision": "Removed currency symbols and commas, then converted to numeric"
    },

    {
        "area": "dates",
        "decision": "Parsed host, calendar, and review dates using pandas datetime"
    },

    {
        "area": "text fields",
        "decision": "Trimmed spaces and standardized text fields"
    },

    {
        "area": "missing names",
        "decision": "Filled missing listing and host names with Unknown"
    },

    {
        "area": "review fields",
        "decision": "Filled missing review count and reviews per month with 0"
    },

    {
        "area": "review scores",
        "decision": "Kept missing review scores as null"
    },

    {
        "area": "geography",
        "decision": "Added city name and rounded coordinates to 5 decimal places"
    },

    {
        "area": "invalid records",
        "decision": "Flagged invalid records instead of deleting them"
    }

]

pd.DataFrame(cleaning_decisions).to_csv(
    reports_folder / "cleaning_decision_log.csv",
    index=False
)


print("Transform step completed.")
print("Clean files saved in data/processed/")
print("Reports saved:")
print("- reports/generated_csv/cleaning_summary.csv")
print("- reports/generated_csv/validation_summary.csv")
print("- reports/generated_csv/cleaning_decision_log.csv")