from pathlib import Path
import pandas as pd

# File paths
processed_folder = Path("data/processed")
documentation_folder = Path("reports/documentation")
exports_folder = Path("exports")

documentation_folder.mkdir(parents=True, exist_ok=True)
exports_folder.mkdir(parents=True, exist_ok=True)

print("Starting open innovation analysis...\n")


# Read data
listing_master = pd.read_csv(
    processed_folder / "listing_master.csv",
    low_memory=False
)

neighbourhood_summary = pd.read_csv(
    processed_folder / "neighbourhood_summary.csv",
    low_memory=False
)


# Make sure numeric columns are numeric
# Numeric column expected in listing_master
numeric_columns = [
    "price_clean",
    "review_scores_rating",
    "review_count",
    "occupancy_rate",
    "estimated_revenue"
]

# Convert available listing-level numeric columns into numeric format
for column in numeric_columns:
    if column in listing_master.columns:
        listing_master[column] = pd.to_numeric(
            listing_master[column],
            errors="coerce"
        )

summary_numeric_columns = [
    "listing_count",
    "avg_price",
    "median_price",
    "avg_rating",
    "avg_occupancy"
]

for column in summary_numeric_columns:
    if column in neighbourhood_summary.columns:
        neighbourhood_summary[column] = pd.to_numeric(
            neighbourhood_summary[column],
            errors="coerce"
        )


# Basic market values
overall_median_price = listing_master["price_clean"].median()
overall_avg_rating = listing_master["review_scores_rating"].mean()
overall_avg_occupancy = listing_master["occupancy_rate"].mean()

# Use median_price if available, otherwise avg_price
if "median_price" in neighbourhood_summary.columns:
    neighbourhood_price_column = "median_price"
else:
    neighbourhood_price_column = "avg_price"


# 1. Value neighbourhoods
# Neighbourhoods with lower price but good ratings
value_neighbourhoods = neighbourhood_summary[
    (neighbourhood_summary["listing_count"] >= 20) &
    (neighbourhood_summary[neighbourhood_price_column] < overall_median_price) &
    (neighbourhood_summary["avg_rating"] >= overall_avg_rating)
].copy()

# Sort value neighbourhoods by rating
value_neighbourhoods = value_neighbourhoods.sort_values(
    by="avg_rating",
    ascending=False
)

# Save value neighbourhoods export
value_neighbourhoods.to_csv(
    exports_folder / "value_neighbourhoods.csv",
    index=False
)


# 2. Premium neighbourhoods
# Neighbourhoods with highest prices
premium_neighbourhoods = neighbourhood_summary.sort_values(
    by=neighbourhood_price_column,
    ascending=False
).head(10)

# Save premium neighbourhoods export
premium_neighbourhoods.to_csv(
    exports_folder / "premium_neighbourhoods.csv",
    index=False
)


# 3. High occupancy neighbourhoods
if "avg_occupancy" in neighbourhood_summary.columns:
    high_occupancy_neighbourhoods = neighbourhood_summary.sort_values(
        by="avg_occupancy",
        ascending=False
    ).head(10)
else:
    high_occupancy_neighbourhoods = pd.DataFrame()

# Save high occupancy neighbourhoods export
high_occupancy_neighbourhoods.to_csv(
    exports_folder / "high_occupancy_neighbourhoods.csv",
    index=False
)


# 4. Listings that may need improvement
# High review count but lower rating
improvement_opportunities = listing_master[
    (listing_master["review_count"] >= 20) &
    (listing_master["review_scores_rating"] < 4.5)
].copy()

# Keep top 20 listings by review count
improvement_opportunities = improvement_opportunities.sort_values(
    by="review_count",
    ascending=False
).head(20)

# Select important columns for improvement export
improvement_columns = [
    "listing_id",
    "name",
    "host_name",
    "neighbourhood_cleansed",
    "room_type",
    "price_clean",
    "review_count",
    "review_scores_rating"
]

improvement_opportunities[improvement_columns].to_csv(
    exports_folder / "improvement_opportunities.csv",
    index=False
)


# 5. Top estimated revenue listings
top_revenue_listings = listing_master[
    listing_master["estimated_revenue"].notna()
].sort_values(
    by="estimated_revenue",
    ascending=False
).head(20)

# Select important columns for revenue export
revenue_columns = [
    "listing_id",
    "name",
    "host_name",
    "neighbourhood_cleansed",
    "room_type",
    "price_clean",
    "occupancy_rate",
    "estimated_revenue"
]

top_revenue_listings[revenue_columns].to_csv(
    exports_folder / "top_estimated_revenue_listings.csv",
    index=False
)


# Create simple markdown report
report_path = documentation_folder / "section_8_open_innovation.md"

with open(report_path, "w", encoding="utf-8") as report:
    report.write("# Section 8 — Open Innovation Challenge\n\n")

    report.write("## Mini Airbnb Market Opportunity Finder\n\n")

    report.write(
        "For the Open Innovation Challenge, I created a small rule-based market opportunity report. "
        "The goal is to help a business user quickly identify useful neighbourhood and listing-level opportunities from the processed Airbnb data.\n\n"
    )

    report.write("This is not a machine learning model. It is a simple business insight layer built on top of the cleaned and enriched dataset.\n\n")

    report.write("## Inputs Used\n\n")
    report.write("- `data/processed/listing_master.csv`\n")
    report.write("- `data/processed/neighbourhood_summary.csv`\n\n")

    report.write("## Outputs Created\n\n")
    report.write("- `exports/value_neighbourhoods.csv`\n")
    report.write("- `exports/premium_neighbourhoods.csv`\n")
    report.write("- `exports/high_occupancy_neighbourhoods.csv`\n")
    report.write("- `exports/improvement_opportunities.csv`\n")
    report.write("- `exports/top_estimated_revenue_listings.csv`\n\n")

    report.write("## Market Summary\n\n")
    report.write(f"- Overall median listing price: {round(overall_median_price, 2)}\n")
    report.write(f"- Overall average review rating: {round(overall_avg_rating, 2)}\n")
    report.write(f"- Overall average occupancy rate: {round(overall_avg_occupancy, 2)}\n\n")

    report.write("## 1. Value Neighbourhoods\n\n")
    report.write(
        "Value neighbourhoods are areas where prices are below the overall median price, "
        "but ratings are equal to or above the overall average rating.\n\n"
    )
    report.write(f"Number of value neighbourhoods found: {len(value_neighbourhoods)}\n\n")
    report.write("Output file: `exports/value_neighbourhoods.csv`\n\n")

    report.write("## 2. Premium Neighbourhoods\n\n")
    report.write(
        "Premium neighbourhoods are the neighbourhoods with the highest prices. "
        "These areas may represent stronger pricing power or more desirable locations.\n\n"
    )
    report.write("Output file: `exports/premium_neighbourhoods.csv`\n\n")

    report.write("## 3. High Occupancy Neighbourhoods\n\n")
    report.write(
        "High occupancy neighbourhoods are areas where listings show higher estimated occupancy rates. "
        "This may indicate stronger demand, although occupancy is only an estimate based on calendar availability.\n\n"
    )
    report.write("Output file: `exports/high_occupancy_neighbourhoods.csv`\n\n")

    report.write("## 4. Improvement Opportunities\n\n")
    report.write(
        "These are listings with many reviews but lower review scores. "
        "They may be useful for identifying listings where guest experience improvements could have business value.\n\n"
    )
    report.write(f"Number of improvement opportunity listings found: {len(improvement_opportunities)}\n\n")
    report.write("Output file: `exports/improvement_opportunities.csv`\n\n")

    report.write("## 5. Top Estimated Revenue Listings\n\n")
    report.write(
        "These listings have the highest estimated revenue based on listing price and estimated occupancy. "
        "This is only an estimate, not confirmed revenue.\n\n"
    )
    report.write("Output file: `exports/top_estimated_revenue_listings.csv`\n\n")

    report.write("## Business Value\n\n")
    report.write(
        "This small feature turns the cleaned dataset into a simple business-facing insight report. "
        "Instead of only showing raw tables and charts, it highlights possible areas of opportunity for hosts, analysts, or market strategists.\n\n"
    )

    report.write("## Limitation\n\n")
    report.write(
        "The opportunity labels are based on simple rules, not machine learning. "
        "Revenue and occupancy values are estimates because unavailable calendar days may include both booked days and host-blocked days.\n"
    )

print("Open innovation analysis completed.")
print("Files created:")
print("- reports/documentation/section_8_open_innovation.md")
print("- exports/value_neighbourhoods.csv")
print("- exports/premium_neighbourhoods.csv")
print("- exports/high_occupancy_neighbourhoods.csv")
print("- exports/improvement_opportunities.csv")
print("- exports/top_estimated_revenue_listings.csv")