from pathlib import Path
import pandas as pd
from scipy import stats

# File paths
processed_folder = Path("data/processed")
reports_folder = Path("reports/generated_csv")
reports_folder.mkdir(parents=True, exist_ok=True)

print("Starting statistical analysis...\n")

# Read master data
listing_master = pd.read_csv(
    processed_folder / "listing_master.csv",
    low_memory=False
)

# Make sure numeric columns are numeric
listing_master["price_clean"] = pd.to_numeric(
    listing_master["price_clean"],
    errors="coerce"
)

listing_master["review_scores_rating"] = pd.to_numeric(
    listing_master["review_scores_rating"],
    errors="coerce"
)

listing_master["review_count"] = pd.to_numeric(
    listing_master["review_count"],
    errors="coerce"
)

# Clean superhost column
listing_master["host_is_superhost_clean"] = (
    listing_master["host_is_superhost"]
    .astype(str)
    .str.lower()
    .map({
        "true": True,
        "false": False,
        "t": True,
        "f": False
    })
)

results = []

# Helper for simple interpretation
def result_text(p_value):
    if p_value < 0.05:
        return "Statistically significant difference found."
    else:
        return "No statistically significant difference found."



# H1: Entire homes vs private rooms price
# Select valid prices for entire homes
entire_home_prices = listing_master[
    (listing_master["room_type"] == "Entire home/apt") &
    (listing_master["price_clean"].notna()) &
    (listing_master["price_clean"] > 0)
]["price_clean"]

# Select valid prices for private rooms
private_room_prices = listing_master[
    (listing_master["room_type"] == "Private room") &
    (listing_master["price_clean"].notna()) &
    (listing_master["price_clean"] > 0)
]["price_clean"]

# Run test only if both groups have data
if len(entire_home_prices) > 0 and len(private_room_prices) > 0:
    statistic, p_value = stats.mannwhitneyu(
        entire_home_prices,
        private_room_prices,
        alternative="two-sided"
    )

    results.append({
        "hypothesis": "H1",
        "question": "Do entire homes and private rooms have different prices?",
        "test_used": "Mann-Whitney U test",
        "group_1": "Entire home/apt",
        "group_2": "Private room",
        "group_1_count": len(entire_home_prices),
        "group_2_count": len(private_room_prices),
        "group_1_median": round(entire_home_prices.median(), 2),
        "group_2_median": round(private_room_prices.median(), 2),
        "practical_difference": round(entire_home_prices.median() - private_room_prices.median(), 2),
        "p_value": round(p_value, 6),
        "interpretation": result_text(p_value)
    })



# H2: Superhost vs non-superhost review scores
# Run test only if both groups have data
superhost_scores = listing_master[
    (listing_master["host_is_superhost_clean"] == True) &
    (listing_master["review_scores_rating"].notna())
]["review_scores_rating"]

# Select valid review scores for non-superhost listings
non_superhost_scores = listing_master[
    (listing_master["host_is_superhost_clean"] == False) &
    (listing_master["review_scores_rating"].notna())
]["review_scores_rating"]

# Run test only if both groups have data
if len(superhost_scores) > 0 and len(non_superhost_scores) > 0:
    statistic, p_value = stats.mannwhitneyu(
        superhost_scores,
        non_superhost_scores,
        alternative="two-sided"
    )

    results.append({
        "hypothesis": "H2",
        "question": "Do superhost and non-superhost listings have different review scores?",
        "test_used": "Mann-Whitney U test",
        "group_1": "Superhost",
        "group_2": "Non-superhost",
        "group_1_count": len(superhost_scores),
        "group_2_count": len(non_superhost_scores),
        "group_1_median": round(superhost_scores.median(), 2),
        "group_2_median": round(non_superhost_scores.median(), 2),
        "practical_difference": round(superhost_scores.median() - non_superhost_scores.median(), 2),
        "p_value": round(p_value, 6),
        "interpretation": result_text(p_value)
    })



# H3: Listings with >10 reviews vs <=10 reviews price
# Select valid prices for listings with more than 10 reviews
high_review_prices = listing_master[
    (listing_master["review_count"] > 10) &
    (listing_master["price_clean"].notna()) &
    (listing_master["price_clean"] > 0)
]["price_clean"]

# Select valid prices for listings with 10 or fewer reviews
low_review_prices = listing_master[
    (listing_master["review_count"] <= 10) &
    (listing_master["price_clean"].notna()) &
    (listing_master["price_clean"] > 0)
]["price_clean"]

# Run test only if both groups have data
if len(high_review_prices) > 0 and len(low_review_prices) > 0:
    statistic, p_value = stats.mannwhitneyu(
        high_review_prices,
        low_review_prices,
        alternative="two-sided"
    )

    results.append({
        "hypothesis": "H3",
        "question": "Do listings with more than 10 reviews have different prices?",
        "test_used": "Mann-Whitney U test",
        "group_1": "More than 10 reviews",
        "group_2": "10 or fewer reviews",
        "group_1_count": len(high_review_prices),
        "group_2_count": len(low_review_prices),
        "group_1_median": round(high_review_prices.median(), 2),
        "group_2_median": round(low_review_prices.median(), 2),
        "practical_difference": round(high_review_prices.median() - low_review_prices.median(), 2),
        "p_value": round(p_value, 6),
        "interpretation": result_text(p_value)
    })



# H4: Price differences across neighbourhoods
# Keep only valid positive price records
price_data = listing_master[
    (listing_master["price_clean"].notna()) &
    (listing_master["price_clean"] > 0)
].copy()

# Select top 5 neighbourhoods 
top_neighbourhoods = (
    price_data["neighbourhood_cleansed"]
    .value_counts()
    .head(5)
    .index
)

groups = []

# Create one price group per neighbourhood
for neighbourhood in top_neighbourhoods:
    group_prices = price_data[
        price_data["neighbourhood_cleansed"] == neighbourhood
    ]["price_clean"]

    if len(group_prices) > 1:
        groups.append(group_prices)

if len(groups) >= 2:
    statistic, p_value = stats.f_oneway(*groups)

    results.append({
        "hypothesis": "H4",
        "question": "Do prices differ across major neighbourhoods?",
        "test_used": "One-way ANOVA",
        "group_1": "Top 5 neighbourhoods",
        "group_2": "Not applicable",
        "group_1_count": len(price_data[price_data["neighbourhood_cleansed"].isin(top_neighbourhoods)]),
        "group_2_count": "",
        "group_1_median": "",
        "group_2_median": "",
        "practical_difference": "Neighbourhood price differences tested",
        "p_value": round(p_value, 6),
        "interpretation": result_text(p_value)
    })



# H5: Weekend vs weekday price
results.append({
    "hypothesis": "H5",
    "question": "Are weekend and weekday prices different?",
    "test_used": "Not performed",
    "group_1": "Weekend",
    "group_2": "Weekday",
    "group_1_count": "",
    "group_2_count": "",
    "group_1_median": "",
    "group_2_median": "",
    "practical_difference": "",
    "p_value": "",
    "interpretation": "This test was not performed because calendar price and adjusted_price are missing in the Amsterdam dataset."
})



# Save results
results_df = pd.DataFrame(results)

results_df.to_csv(
    reports_folder / "statistical_test_results.csv",
    index=False
)

print("Statistical analysis completed.")
print("Report created:")
print("reports/generated_csv/statistical_test_results.csv")