-- Nettoyage des avis
-- Génération d'un id artificiel via ROW_NUMBER()
-- Conversion date TIMESTAMP WITH TIME ZONE → DATE pour jointure pleine lune
-- Remplacement des sentiments NULL par 'unknown'
SELECT
    ROW_NUMBER() OVER (ORDER BY r.listing_id, r.date)  AS review_id,
    r.listing_id,
    CAST(r.date AS DATE)                               AS review_date,
    TRIM(r.reviewer_name)                              AS reviewer_name,
    r.comments,
    COALESCE(r.sentiment, 'unknown')                   AS sentiment,
    CASE
        WHEN fm.full_moon_date IS NOT NULL THEN TRUE
        ELSE FALSE
    END                                                AS is_full_moon_review
FROM {{ ref('bronze_reviews') }} r
LEFT JOIN {{ ref('seed_full_moon_dates') }} fm
    ON CAST(r.date AS DATE) = fm.full_moon_date
WHERE r.listing_id IS NOT NULL
    AND r.date IS NOT NULL