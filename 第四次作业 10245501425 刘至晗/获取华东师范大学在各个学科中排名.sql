WITH DisciplineMinId AS (
    SELECT 
        discipline, 
        MIN(id) AS min_discipline_id
    FROM esi_combined
    GROUP BY discipline
)

SELECT 
    e.discipline,
    e.Institutions,
    (e.id - d.min_discipline_id) + 1 AS rank_by_id
FROM esi_combined e
JOIN (
    SELECT 
        discipline, 
        MIN(id) AS min_discipline_id
    FROM esi_combined
    GROUP BY discipline
) d ON e.discipline = d.discipline
WHERE e.Institutions = 'East China Normal University'
ORDER BY e.discipline, rank_by_id;