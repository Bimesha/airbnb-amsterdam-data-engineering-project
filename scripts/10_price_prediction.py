from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# File path
processed_folder = Path("data/processed")
reports_folder = Path("reports/generated_csv")
figures_folder = Path("figures")

reports_folder.mkdir(parents=True, exist_ok=True)
figures_folder.mkdir(parents=True, exist_ok=True)

print("Starting simple price prediction model...\n")


# Read data
df = pd.read_csv(
    processed_folder / "listing_master.csv",
    low_memory=False
)

# Prepare target column
df["price_clean"] = pd.to_numeric(df["price_clean"], errors="coerce")

# Keep only valid prices
df = df[
    (df["price_clean"].notna()) &
    (df["price_clean"] > 0)
].copy()

# Remove very high price outliers for a simpler model
price_limit = df["price_clean"].quantile(0.99)
df = df[df["price_clean"] <= price_limit].copy()


# Create fallback review column
if "review_count" not in df.columns:
    df["review_count"] = df["number_of_reviews"]


# Select simple features
features = [
    "room_type",
    "property_type",
    "neighbourhood_cleansed",
    "accommodates",
    "bedrooms",
    "beds",
    "availability_365",
    "review_scores_rating",
    "review_count",
    "occupancy_rate"
]

# Keep only columns that exist
features = [col for col in features if col in df.columns]

model_data = df[features + ["price_clean"]].copy()


# Handle missing values
for column in model_data.columns:
    if column == "price_clean":
        continue

    if model_data[column].dtype == "object":
        model_data[column] = model_data[column].fillna("Unknown")
    else:
        model_data[column] = pd.to_numeric(model_data[column], errors="coerce")
        model_data[column] = model_data[column].fillna(model_data[column].median())


# Encode categorical columns
X = model_data.drop(columns=["price_clean"])
y = model_data["price_clean"]

X = pd.get_dummies(X, drop_first=True)


# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10
    )
}

results = []

kfold = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# Train and evaluate models
for model_name, model in models.items():
    print(f"Training {model_name}...")

    cv_scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=kfold,
        scoring="neg_mean_absolute_error"
    )

    cv_mae = -cv_scores.mean()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    results.append({
        "model": model_name,
        "cross_validation_mae": round(cv_mae, 2),
        "test_mae": round(mae, 2),
        "test_rmse": round(rmse, 2),
        "test_r2": round(r2, 4)
    })


# Save model comparison
results_df = pd.DataFrame(results)

results_df.to_csv(
    reports_folder / "price_prediction_results.csv",
    index=False
)


# Feature importance from Random Forest
rf_model = models["Random Forest"]

feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": rf_model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
).head(15)

feature_importance.to_csv(
    reports_folder / "price_prediction_feature_importance.csv",
    index=False
)


# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(feature_importance["feature"], feature_importance["importance"])
plt.title("Top Features for Price Prediction")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(figures_folder / "price_prediction_feature_importance.png")
plt.close()

print("Price prediction completed.")
print("Reports created:")
print("- reports/generated_csv/price_prediction_results.csv")
print("- reports/generated_csv/price_prediction_feature_importance.csv")
print("- figures/price_prediction_feature_importance.png")