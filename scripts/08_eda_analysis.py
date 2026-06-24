from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# Folder paths
processed_folder = Path("data/processed")
reports_folder = Path("reports/generated_csv")
figures_folder = Path("figures")

reports_folder.mkdir(parents=True, exist_ok=True)
figures_folder.mkdir(exist_ok=True)


print("Starting EDA analysis...\n")


# Read input data
listing_master = pd.read_csv(
    processed_folder / "listing_master.csv",
    low_memory=False
)


# Read cleaned calendar dataset
calendar = pd.read_csv(
    processed_folder / "clean_calendar.csv",
    low_memory=False
)



# Prepare price data
# Convert price column into numeric format
listing_master["price_clean"] = pd.to_numeric(
    listing_master["price_clean"],
    errors="coerce"
)

# Keep only valid positive price records
price_data = listing_master[
    (listing_master["price_clean"].notna()) &
    (listing_master["price_clean"] > 0)
].copy()


# Identify very high prices using the 99th percentile threshold
price_limit = price_data["price_clean"].quantile(0.99)


# Flag price records above the 99th percentile as EDA outliers
price_data["price_outlier_for_eda"] = price_data["price_clean"] > price_limit


# Create price data without EDA outliers for clearer charts
price_analysis_data = price_data[~price_data["price_outlier_for_eda"]].copy()
price_chart_data = price_analysis_data.copy()


# Create a small outlier summary for documentation
outlier_summary = pd.DataFrame([
    {
        "price_outlier_threshold_99th_percentile": round(price_limit, 2),
        "valid_price_records": len(price_data),
        "outlier_records": int(price_data["price_outlier_for_eda"].sum()),
        "records_used_for_eda_charts": len(price_analysis_data)
    }
])


# Save price outlier summary report
outlier_summary.to_csv(
    reports_folder / "eda_price_outlier_summary.csv",
    index=False
)


# 1. Price distribution
# Create histogram for price distribution without EDA outliers
plt.figure(figsize=(8, 5))
plt.hist(price_chart_data["price_clean"], bins=40)
plt.title("Amsterdam Airbnb Price Distribution")
plt.xlabel("Price")
plt.ylabel("Number of Listings")
plt.tight_layout()
plt.savefig(figures_folder / "price_distribution.png")
plt.close()



# 2. Price by room type
# Calculate room-level median and raw average using all valid prices
room_median = (
    price_data
    .groupby("room_type")
    .agg(
        listing_count=("listing_id", "count"),
        median_price=("price_clean", "median"),
        raw_average_price=("price_clean", "mean"),
        outlier_count=("price_outlier_for_eda", "sum"),
        max_price_before_filter=("price_clean", "max")
    )
    .reset_index()
)

# Calculate room-level average after excluding EDA outliers
room_average = (
    price_analysis_data
    .groupby("room_type")
    .agg(
        average_price=("price_clean", "mean")
    )
    .reset_index()
)

# Combine room-level raw and filtered summaries
room_type_summary = room_median.merge(
    room_average,
    on="room_type",
    how="left"
)

# Reorder room type summary columns
room_type_summary = room_type_summary[[
    "room_type",
    "listing_count",
    "median_price",
    "average_price",
    "outlier_count",
    "raw_average_price",
    "max_price_before_filter"
]]


# Round numeric columns for cleaner reporting
round_columns = [
    "median_price",
    "average_price",
    "raw_average_price",
    "max_price_before_filter"
]

for column in round_columns:
    room_type_summary[column] = room_type_summary[column].round(2)


# Save room type summary report
room_type_summary.to_csv(
    reports_folder / "eda_room_type_summary.csv",
    index=False
)


# Create bar chart for median price by room type
plt.figure(figsize=(8, 5))
plt.bar(room_type_summary["room_type"], room_type_summary["median_price"])
plt.title("Median Price by Room Type")
plt.xlabel("Room Type")
plt.ylabel("Median Price")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figures_folder / "price_by_room_type.png")
plt.close()



# 3. Top neighbourhoods by median price
# Calculate neighbourhood price and rating summary
neighbourhood_price = (
    price_data
    .groupby("neighbourhood_cleansed")
    .agg(
        listing_count=("listing_id", "count"),
        median_price=("price_clean", "median"),
        average_rating=("review_scores_rating", "mean")
    )
    .reset_index()
)


# Keep only neighbourhoods with at least 20 listings
neighbourhood_price = neighbourhood_price[
    neighbourhood_price["listing_count"] >= 20
]


# Round neighbourhood summary values
neighbourhood_price["median_price"] = neighbourhood_price["median_price"].round(2)
neighbourhood_price["average_rating"] = neighbourhood_price["average_rating"].round(2)


# Select top 10 neighbourhoods by median price
top_neighbourhoods = neighbourhood_price.sort_values(
    by="median_price",
    ascending=False
).head(10)


# Save neighbourhood summary report
neighbourhood_price.to_csv(
    reports_folder / "eda_neighbourhood_price_summary.csv",
    index=False
)


# Create bar chart for top neighbourhoods by median price
plt.figure(figsize=(10, 5))
plt.bar(
    top_neighbourhoods["neighbourhood_cleansed"],
    top_neighbourhoods["median_price"]
)
plt.title("Top 10 Neighbourhoods by Median Price")
plt.xlabel("Neighbourhood")
plt.ylabel("Median Price")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(figures_folder / "top_neighbourhoods_by_price.png")
plt.close()



# 4. Monthly availability
# Convert calendar date into datetime format
calendar["date"] = pd.to_datetime(
    calendar["date"],
    errors="coerce"
)

# Convert availability values into numeric values
calendar["available_number"] = calendar["is_available"].astype(str).str.lower().map({
    "true": 1,
    "false": 0,
    "t": 1,
    "f": 0
})

# Extract month from date
calendar["month"] = calendar["date"].dt.to_period("M").astype(str)


# Calculate average availability by month
monthly_availability = (
    calendar
    .groupby("month")
    .agg(
        average_availability=("available_number", "mean")
    )
    .reset_index()
)


# Convert average availability into percentage
monthly_availability["average_availability"] = (
    monthly_availability["average_availability"] * 100
).round(2)


# Save monthly availability report
monthly_availability.to_csv(
    reports_folder / "eda_monthly_availability.csv",
    index=False
)


# Create monthly availability line chart
plt.figure(figsize=(10, 5))
plt.plot(
    monthly_availability["month"],
    monthly_availability["average_availability"],
    marker="o"
)
plt.title("Average Monthly Availability")
plt.xlabel("Month")
plt.ylabel("Average Availability (%)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(figures_folder / "monthly_availability.png")
plt.close()



# 5. Host listing count analysis
# Calculate listing count and average price by host
host_summary = (
    listing_master
    .groupby(["host_id", "host_name"])
    .agg(
        listing_count=("listing_id", "count"),
        average_price=("price_clean", "mean")
    )
    .reset_index()
)

# Round average price for reporting
host_summary["average_price"] = host_summary["average_price"].round(2)


# Save host summary report
host_summary.to_csv(
    reports_folder / "eda_host_summary.csv",
    index=False
)

# Select top 10 hosts by number of listings
top_hosts = host_summary.sort_values(
    by="listing_count",
    ascending=False
).head(10)


# Create top hosts bar chart
plt.figure(figsize=(10, 5))
plt.bar(top_hosts["host_name"].astype(str), top_hosts["listing_count"])
plt.title("Top 10 Hosts by Number of Listings")
plt.xlabel("Host")
plt.ylabel("Number of Listings")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(figures_folder / "top_hosts_by_listing_count.png")
plt.close()



# 6. Review score vs price
# Keep records with review scores for scatter plot
review_price = price_chart_data[
    price_chart_data["review_scores_rating"].notna()
].copy()

# Use a sample if there are many records
if len(review_price) > 2000:
    review_price = review_price.sample(2000, random_state=42)

# Create scatter plot for review score vs price
plt.figure(figsize=(8, 5))
plt.scatter(
    review_price["price_clean"],
    review_price["review_scores_rating"],
    alpha=0.4
)
plt.title("Review Score vs Price")
plt.xlabel("Price")
plt.ylabel("Review Score")
plt.tight_layout()
plt.savefig(figures_folder / "review_score_vs_price.png")
plt.close()


# 7. Simple summary report
# Create overall EDA summary
eda_summary = {
    "total_listings": len(listing_master),
    "listings_with_price": len(price_data),
    "median_price": round(price_data["price_clean"].median(), 2),
    "average_price": round(price_data["price_clean"].mean(), 2),
    "average_price_without_eda_outliers": round(price_analysis_data["price_clean"].mean(), 2),
    "average_review_score": round(listing_master["review_scores_rating"].mean(), 2),
    "average_occupancy_rate": round(listing_master["occupancy_rate"].mean(), 2)
}

# Convert EDA summary into a DataFrame
eda_summary_df = pd.DataFrame([eda_summary])

# Save EDA summary report
eda_summary_df.to_csv(
    reports_folder / "eda_summary.csv",
    index=False
)

print("EDA analysis completed.")
print("Reports created in reports/generated_csv folder.")
print("Figures created in figures folder.")
print("Price outlier summary saved: reports/generated_csv/eda_price_outlier_summary.csv")