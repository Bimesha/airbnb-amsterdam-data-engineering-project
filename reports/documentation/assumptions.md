# Assumptions

The following assumptions were used throughout the project:

1. `listings.id` is the main unique listing identifier.
2. `calendar.listing_id` links calendar rows back to `listings.id`.
3. `reviews.listing_id` links review rows back to `listings.id`.
4. `calendar.available = t` means the listing is available on that date.
5. `calendar.available = f` means the listing is unavailable, but it does not confirm that the listing was booked.
6. Listing-level `price` is used for price analysis because calendar price fields were missing.
7. Estimated occupancy is calculated from calendar availability and should be treated as approximate.
8. Estimated revenue is not actual Airbnb revenue; it is an analytical estimate.
9. Review count and reviews per month are used as demand proxies, not exact booking counts.
10. Missing review scores are kept as null values to avoid changing rating analysis.
11. Amsterdam is the only city analyzed, so cross-city comparison is outside the project scope.
