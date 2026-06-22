-- Analyse des hôtes : superhosts vs hôtes classiques
SELECT
    h.is_superhost,
    COUNT(DISTINCT h.host_id)           AS nb_hotes,
    COUNT(l.listing_id)                 AS nb_logements,
    ROUND(AVG(l.price), 2)              AS prix_moyen,
    ROUND(MIN(l.price), 2)              AS prix_min,
    ROUND(MAX(l.price), 2)              AS prix_max
FROM {{ ref('silver_hosts') }} h
LEFT JOIN {{ ref('silver_listings') }} l
    ON h.host_id = l.host_id
GROUP BY 1
ORDER BY 1