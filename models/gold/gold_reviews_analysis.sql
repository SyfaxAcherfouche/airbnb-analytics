-- Analyse des avis par mois et sentiment
SELECT
    DATE_TRUNC('month', review_date)    AS mois,
    sentiment,
    COUNT(*)                            AS nb_avis,
    SUM(CASE WHEN is_full_moon_review
        THEN 1 ELSE 0 END)              AS nb_avis_pleine_lune
FROM {{ ref('silver_reviews') }}
GROUP BY 1, 2
ORDER BY 1, 2