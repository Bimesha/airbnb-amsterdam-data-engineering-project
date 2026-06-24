# Section 5 - Statistical Analysis

Basic statistical tests were used to check whether selected Airbnb market patterns were statistically meaningful.

## Tests Completed

| Hypothesis | Test Used | Result |
|---|---|---|
| Entire homes/apartments have different prices than private rooms | Mann-Whitney U | Significant difference found |
| Superhost and non-superhost listings have different review scores | Mann-Whitney U | Significant difference found, but practical difference is small |
| Listings with more than 10 reviews have different prices than listings with 10 or fewer reviews | Mann-Whitney U | Significant difference found |
| Prices differ across major neighbourhoods | One-way ANOVA | Significant difference found |
| Weekend prices differ from weekday prices | Not performed | Calendar price fields were missing |

## Business Interpretation

The statistical results support the EDA findings that listing type, review activity, and neighbourhood are related to Airbnb pricing. However, statistical significance does not always mean the result is large enough to be a major business decision by itself.

The superhost comparison showed a statistically significant difference in review scores, but the rating difference was small. This means the result should be interpreted carefully in business terms.

## Limitation

The weekday versus weekend pricing test could not be completed because the calendar `price` and `adjusted_price` fields were missing.
