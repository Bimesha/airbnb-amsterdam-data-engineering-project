
-- Airbnb Amsterdam Analysis Queries

-- 1. Check table row counts
SELECT 'dim_host' AS table_name, COUNT(*) AS row_count
FROM analytics.dim_host
UNION ALL
SELECT 'dim_listing', COUNT(*)
FROM analytics.dim_listing
UNION ALL
SELECT 'dim_neighbourhood', COUNT(*)
FROM analytics.dim_neighbourhood
UNION ALL
SELECT 'fact_listing_performance', COUNT(*)
FROM analytics.fact_listing_performance
UNION ALL
SELECT 'listing_master', COUNT(*)
FROM analytics.listing_master
UNION ALL
SELECT 'calendar_summary', COUNT(*)
FROM analytics.calendar_summary
UNION ALL
SELECT 'review_summary', COUNT(*)
FROM analytics.review_summary
UNION ALL
SELECT 'neighbourhood_summary', COUNT(*)
FROM analytics.neighbourhood_summary;


-- 2. Average price by room type
SELECT
    l.room_type,
    COUNT(*) AS listing_count,
    ROUND(AVG(f.price_clean)::numeric, 2) AS average_price,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.price_clean)::numeric, 2) AS median_price
FROM analytics.fact_listing_performance f
JOIN analytics.dim_listing l
    ON f.listing_id = l.listing_id
WHERE f.price_clean IS NOT NULL
GROUP BY l.room_type
ORDER BY median_price DESC;


-- 3. Neighbourhood price and rating summary
SELECT
    n.neighbourhood_cleansed,
    COUNT(*) AS listing_count,
    ROUND(AVG(f.price_clean)::numeric, 2) AS average_price,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.price_clean)::numeric, 2) AS median_price,
    ROUND(AVG(f.review_scores_rating)::numeric, 2) AS average_rating,
    ROUND(AVG(f.occupancy_rate)::numeric, 2) AS average_estimated_occupancy
FROM analytics.fact_listing_performance f
JOIN analytics.dim_neighbourhood n
    ON f.neighbourhood_id = n.neighbourhood_id
WHERE f.price_clean IS NOT NULL
GROUP BY n.neighbourhood_cleansed
ORDER BY median_price DESC;


-- 4. Top hosts by number of listings
SELECT
    h.host_id,
    h.host_name,
    COUNT(l.listing_id) AS listing_count
FROM analytics.dim_host h
JOIN analytics.dim_listing l
    ON h.host_id = l.host_id
GROUP BY
    h.host_id,
    h.host_name
ORDER BY listing_count DESC
LIMIT 10;


-- 5. Top listings by estimated revenue
SELECT
    l.listing_id,
    l.name,
    l.room_type,
    n.neighbourhood_cleansed,
    f.price_clean,
    f.occupancy_rate AS estimated_occupancy_rate,
    f.estimated_revenue AS estimated_annual_revenue
FROM analytics.fact_listing_performance f
JOIN analytics.dim_listing l
    ON f.listing_id = l.listing_id
JOIN analytics.dim_neighbourhood n
    ON f.neighbourhood_id = n.neighbourhood_id
WHERE f.estimated_revenue IS NOT NULL
ORDER BY f.estimated_revenue DESC
LIMIT 20;


-- 6. Review score by room type
SELECT
    l.room_type,
    COUNT(*) AS listing_count,
    ROUND(AVG(f.review_scores_rating)::numeric, 2) AS average_review_score,
    ROUND(AVG(f.review_count)::numeric, 2) AS average_review_count
FROM analytics.fact_listing_performance f
JOIN analytics.dim_listing l
    ON f.listing_id = l.listing_id
WHERE f.review_scores_rating IS NOT NULL
GROUP BY l.room_type
ORDER BY average_review_score DESC;


-- 7. Price per bedroom by room type
SELECT
    l.room_type,
    COUNT(*) AS listing_count,
    ROUND(AVG(f.price_per_bedroom)::numeric, 2) AS average_price_per_bedroom
FROM analytics.fact_listing_performance f
JOIN analytics.dim_listing l
    ON f.listing_id = l.listing_id
WHERE f.price_per_bedroom IS NOT NULL
GROUP BY l.room_type
ORDER BY average_price_per_bedroom DESC;
