-- Nettoyage des logements
-- Conversion du prix : "$90.00" → 90.0
-- Normalisation des timestamps avec timezone en DATE
SELECT
    id                                                          AS listing_id,
    TRIM(name)                                                  AS listing_name,
    listing_url,
    host_id,
    TRIM(room_type)                                             AS room_type,
    minimum_nights,
    CAST(
        REPLACE(REPLACE(price, '$', ''), ',', '')
        AS FLOAT
    )                                                           AS price,
    CAST(created_at AS DATE)                                   AS created_at,
    CAST(updated_at AS DATE)                                   AS updated_at
FROM {{ ref('bronze_listings') }}
WHERE id IS NOT NULL
    AND host_id IS NOT NULL
    AND price IS NOT NULL
    AND price != '$0.00'