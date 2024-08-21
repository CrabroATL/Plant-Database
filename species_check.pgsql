SELECT COUNT(species_id), family FROM species 
JOIN family ON 
family.family_id = species.family_id  
WHERE species.phyla_id = --PHYLA ID
GROUP BY family.family_id 
ORDER BY family;

SELECT COUNT(species_id), genera FROM species JOIN genera ON 
genera.genera_id = species.genera_id 
JOIN family ON family.family_id = species.family_id 
WHERE species.phyla_id = --PHYLA ID
AND family = --FAMILY NAME
GROUP BY genera.genera_id ORDER BY genera;