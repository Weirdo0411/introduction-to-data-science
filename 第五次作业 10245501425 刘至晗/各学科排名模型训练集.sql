WITH DisciplineRank AS (
    SELECT 
        discipline,
        Institutions,
        Cites,
        Top_Papers,
        Cites_Per_Paper,
        DENSE_RANK() OVER (PARTITION BY discipline ORDER BY Cites DESC) AS rank_position,
        COUNT(*) OVER (PARTITION BY discipline) AS discipline_total,
        ROW_NUMBER() OVER (PARTITION BY discipline ORDER BY Cites DESC) AS row_num
    FROM esi_combined
),
TrainSet AS (
    SELECT 
        discipline,
        Institutions,
        Cites,
        Top_Papers,
        Cites_Per_Paper,
        rank_position
    FROM DisciplineRank
    WHERE row_num <= FLOOR(discipline_total * 0.6)
)
SELECT * FROM TrainSet;