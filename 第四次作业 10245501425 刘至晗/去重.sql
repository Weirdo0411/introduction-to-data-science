DELETE FROM esi_combined
WHERE id NOT IN (
    SELECT min_id FROM (
        SELECT MIN(id) AS min_id
        FROM esi_combined
        GROUP BY 
            discipline, 
            Institutions, 
            `Countries/Regions`,  
            `Web of Science Doc`, 
            Cites, 
            `Cites_Per_Paper`,  
            `Top_Papers`  
    ) AS temp
);