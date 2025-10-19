SELECT 
    discipline, 
    Institutions, 
    Cites, 
    COUNT(*) AS record_count
FROM esi_combined
WHERE Institutions = 'East China Normal University'
  AND discipline = 'agricultural_sciences'
GROUP BY discipline, Institutions, Cites
HAVING COUNT(*) > 1;