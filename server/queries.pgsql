SELECT common_name, scientific_name, genera, family, polyphylactic_group, county_name, native, endemic, special_concern, introduced, invasive FROM species
JOIN genera ON genera.genera_id = species.genera_id
JOIN family ON family.family_id = species.family_id
JOIN phyla ON phyla.phyla_id = species.phyla_id
JOIN county_occurance ON county_occurance.species_id = species.species_id
JOIN counties ON counties.county_id = county_occurance.county_id
WHERE common_name LIKE %s AND
scientific_name LIKE %s AND
genera = %s AND
family = %s AND
polyphylactic_group = %s AND
county_name IN %s;
