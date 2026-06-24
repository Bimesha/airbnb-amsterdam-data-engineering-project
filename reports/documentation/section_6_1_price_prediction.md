# Section 6.1 - Price Prediction Experiment

A simple price prediction experiment was completed using the cleaned listing-level price as the target variable.

## Objective

The objective was to test whether basic listing features could be used to predict Airbnb listing prices in Amsterdam.

## Target Variable

- `price_clean`

## Features Used

The model used selected listing features such as:

- room type
- property type
- neighbourhood
- accommodates
- bedrooms
- beds
- availability
- review score
- review count
- estimated occupancy rate

## Models Compared

| Model | Purpose |
|---|---|
| Linear Regression | Simple baseline model |
| Random Forest Regressor | Non-linear comparison model |

## Results

The Random Forest model performed slightly better than Linear Regression. However, the improvement was not large, so the model should be treated as an exploratory experiment rather than a production-ready pricing system.

## Interpretation

Important factors included guest capacity, bedrooms, availability, room type, review count, review score, and estimated occupancy. This matches the business expectation that larger listings and certain room types usually have higher prices.

## Limitation

The model was trained only on available listing-level data. Daily calendar prices were missing, so seasonal or weekday/weekend pricing effects could not be modeled.
