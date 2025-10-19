SELECT 
    discipline, 
    Institutions, 
    SUM(Cites) AS total_cites,  
    AVG(Cites_Per_Paper) AS avg_cites_per_paper,  
    SUM(Top_Papers) AS total_top_papers  
FROM esi_combined
WHERE `Countries/Regions` = 'China Mainland'  
GROUP BY discipline, Institutions
ORDER BY discipline, total_cites DESC;  