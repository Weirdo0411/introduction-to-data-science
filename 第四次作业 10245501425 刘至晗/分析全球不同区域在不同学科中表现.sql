SELECT 
    discipline,  -- 学科
    `Countries/Regions` AS region,  
    SUM(Cites) AS total_cites,  
    SUM(Top_Papers) AS total_top_papers,  
    AVG(Cites_Per_Paper) AS avg_cites_per_paper,  
    RANK() OVER (PARTITION BY discipline ORDER BY SUM(Cites) DESC) AS cite_rank,
    RANK() OVER (PARTITION BY discipline ORDER BY SUM(Top_Papers) DESC) AS top_paper_rank,
    RANK() OVER (PARTITION BY discipline ORDER BY AVG(Cites_Per_Paper) DESC) AS avg_cite_rank
FROM esi_combined
GROUP BY discipline, `Countries/Regions`  
ORDER BY discipline, total_cites DESC;  