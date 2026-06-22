-- Impact des nuits de pleine lune sur les avis
SELECT
    is_full_moon_review,
    sentiment,
    COUNT(*)                            AS nb_avis,
    ROUND(COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (
            PARTITION BY is_full_moon_review
        ), 2)                           AS pct_sentiment
FROM {{ ref('silver_reviews') }}
GROUP BY 1, 2
ORDER BY 1, 2