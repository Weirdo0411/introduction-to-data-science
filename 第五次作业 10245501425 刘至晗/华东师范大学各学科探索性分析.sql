SELECT 
    discipline,
    SUM(`Web of Science Doc`) AS paper_count,
    SUM(Cites) AS total_cites,
    SUM(Top_Papers) AS top_papers
FROM esi_combined
WHERE Institutions = 'East China Normal University'
GROUP BY discipline
ORDER BY total_cites DESC;

WITH GlobalRank AS (
    SELECT 
        e.discipline,
        e.Institutions,
        ROW_NUMBER() OVER (PARTITION BY e.discipline ORDER BY e.id) AS global_rank
    FROM esi_combined e
    WHERE EXISTS (
        SELECT 1 
        FROM esi_combined 
        WHERE Institutions = 'East China Normal University' 
          AND discipline = e.discipline
    )
)
SELECT 
    discipline,
    Institutions,
    global_rank
FROM GlobalRank
WHERE Institutions = 'East China Normal University'
ORDER BY discipline, global_rank;

WITH ChinaRank AS (
    SELECT 
        e.discipline,
        e.Institutions,
        ROW_NUMBER() OVER (PARTITION BY e.discipline ORDER BY e.id) AS china_rank
    FROM esi_combined e
    WHERE e.`Countries/Regions` = 'CHINA MAINLAND'
      AND EXISTS (
        SELECT 1 
        FROM esi_combined 
        WHERE Institutions = 'East China Normal University' 
          AND discipline = e.discipline
    )
)
SELECT 
    discipline,
    Institutions,
    china_rank
FROM ChinaRank
WHERE Institutions = 'East China Normal University'
ORDER BY discipline, china_rank;

SELECT 
    discipline,
    AVG(Cites_Per_Paper) AS 篇均被引,
    SUM(Top_Papers) AS 顶刊数
FROM esi_combined
WHERE Institutions = 'East China Normal University'
GROUP BY discipline
ORDER BY 篇均被引 DESC;