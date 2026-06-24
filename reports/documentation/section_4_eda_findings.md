# Section 4 - Exploratory Data Analysis Findings

Exploratory Data Analysis was performed using the enriched `listing_master` dataset and related summary outputs.

## Dataset Summary

- Total listings: 10,480
- Listings with valid price values: 5,874
- Median listing price: 222.00
- Average listing price: 336.79
- Average listing price after excluding the top 1% EDA price outliers: 252.66
- Average review score: 4.84
- Average estimated occupancy rate: 0.74

## Price Outlier Handling for EDA

The raw listing prices contained a small number of very high values. These records were not deleted from the project dataset, but they were excluded from selected EDA charts and average price summaries so that a few extreme values would not distort interpretation.

The 99th percentile price threshold was used for EDA outlier handling. Median price was still emphasized because it is more stable for skewed price data.

## Price Distribution

The price distribution is right-skewed. Most listings are within a lower to middle price range, while a smaller number of expensive listings increase the average price. For this reason, median price is more reliable than average price when describing typical Airbnb prices.

## Room Type Patterns

Room type is an important pricing factor. Entire homes and apartments generally have higher median prices than private rooms. The hotel room category had a small listing count and some extreme raw price values, so the median price is more reliable than the raw average for that room type.

## Neighbourhood Patterns

Neighbourhood-level analysis showed that prices are not evenly distributed across Amsterdam. Some neighbourhoods have higher median prices, while others appear more affordable. This supports the idea that location is an important factor in Airbnb pricing.

## Availability Patterns

Calendar availability was used to estimate occupancy. However, this should be interpreted carefully because unavailable calendar dates may represent either actual bookings or dates blocked by hosts.

## Host Patterns

Some hosts manage multiple listings, while many hosts manage only one listing. This suggests that the market contains both individual hosts and more professional or portfolio-style hosts.

## Review Score and Price

Review scores were generally high across the dataset. A high rating does not always mean a higher price, because price is also affected by room type, location, capacity, and availability.
