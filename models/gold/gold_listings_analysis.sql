-- Analyse des logements par quartier et type de chambre
SELECT
    room_type,
    COUNT(listing_id)               AS nb_logements,
    ROUND(AVG(price), 2)            AS prix_moyen,
    ROUND(MIN(price), 2)            AS prix_min,
    ROUND(MAX(price), 2)            AS prix_max,
    ROUND(AVG(minimum_nights), 1)   AS minimum_nights_moyen
FROM {{ ref('silver_listings') }}
GROUP BY 1
ORDER BY prix_moyen DESC