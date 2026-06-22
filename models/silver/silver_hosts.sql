-- Nettoyage des hôtes
-- Suppression des 15 lignes sans nom ni statut superhost
SELECT
    id                                      AS host_id,
    TRIM(name)                              AS host_name,
    is_superhost,
    CAST(created_at AS DATE)               AS created_at,
    CAST(updated_at AS DATE)               AS updated_at
FROM {{ ref('bronze_hosts') }}
WHERE id IS NOT NULL
    AND name IS NOT NULL
    AND is_superhost IS NOT NULL