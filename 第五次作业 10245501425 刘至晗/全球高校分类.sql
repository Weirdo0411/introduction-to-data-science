SELECT 
    Institutions,
    CASE 
        WHEN MAX(CASE WHEN (SELECT COUNT(*) FROM (SELECT discipline FROM esi_combined WHERE Institutions = e.Institutions AND rank_by_cites <= 10) AS sub) >= 5 
                       AND e.total_cites >= 1000000 AND e.top_papers >= 100 
                  THEN 1 ELSE 0 END) = 1 
        THEN '综合顶尖型'
        
        WHEN (SELECT COUNT(*) 
              FROM (SELECT discipline 
                    FROM esi_combined 
                    WHERE Institutions = e.Institutions 
                      AND discipline IN (
                          'agricultural sciences','biology & biochemistry','chemistry','computer science','engineering',
                          'immunology','materials science','mathematics',
                          'microbiology','molecular biology & genetics','neuroscience & behavior','pharmacology & toxicology',
                          'physics','plant & animal science'
                      ) 
                      AND rank_by_cites <= 500 
                    GROUP BY discipline) sub) >= 3 
        THEN '理科特色型'
      
        WHEN (SELECT COUNT(*) 
              FROM (SELECT discipline 
                    FROM esi_combined 
                    WHERE Institutions = e.Institutions 
                      AND discipline IN (
                          'clinical medicine','economics & business','psychiatry psychology','social sciences, general',
                          'space science','geosciences','environment ecology'
                      ) 
                      AND rank_by_cites <= 500 
                    GROUP BY discipline) sub) >= 2 
        THEN '文科特色型'
        
        WHEN MAX(CASE WHEN (SELECT COUNT(*) FROM (SELECT discipline FROM esi_combined WHERE Institutions = e.Institutions AND country_rank <= 5) AS sub) >= 10 
                       AND (SELECT COUNT(*) FROM (SELECT discipline FROM esi_combined WHERE Institutions = e.Institutions AND rank_by_cites BETWEEN 50 AND 200) AS sub) >= 10 
                  THEN 1 ELSE 0 END) = 1 
        THEN '区域领先型'
        
        ELSE '均衡发展型'
    END AS uni_type
FROM (
    SELECT 
        Institutions,
        discipline,
        SUM(Cites) AS total_cites,
        SUM(Top_Papers) AS top_papers,
        RANK() OVER (PARTITION BY discipline ORDER BY SUM(Cites) DESC) AS rank_by_cites,
        RANK() OVER (PARTITION BY `Countries/Regions`, discipline ORDER BY SUM(Cites) DESC) AS country_rank
    FROM esi_combined
    GROUP BY Institutions, discipline, `Countries/Regions`
) e
GROUP BY Institutions;