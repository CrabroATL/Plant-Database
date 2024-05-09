-- Create a new table called 'TableName' in schema 'SchemaName'
-- Drop the table if it already exists
CREATE DATABASE plants;

IF OBJECT_ID('plants.phyla', 'U') IS NOT NULL
DROP TABLE plants.phyla
;
-- Create the table in the specified schema
CREATE TABLE plants.phyla
(
    phyla_id INTEGER UNIQUE NOT NULL PRIMARY KEY, -- primary key column
    polyphylactic_group VARCHAR(50) NOT NULL
);

CREATE TABLE plants.family
(
    family_id SERIAL UNIQUE NOT NULL PRIMARY KEY,
    family VARCHAR(50) NOT NULL,
    phyla_id INTEGER REFERENCES phyla (phyla_id) 
);

CREATE TABLE plants.genera
(
    genera_id SERIAL UNIQUE NOT NULL PRIMARY KEY,
    genera VARCHAR(50) NOT NULL,
    family_id INTEGER REFERENCES family (family_id),
    phyla_id INTEGER REFERENCES phyla (phyla_id)
);

-- list of all vascular plant species and relevant data
CREATE TABLE plants.species
(
    species_id SERIAL UNIQUE NOT NULL PRIMARY KEY,
    scientific_name VARCHAR(100) NOT NULL,
    common_name VARCHAR(255) NOT NULL,
    native BOOLEAN,
    endemic BOOLEAN,
    special_concern BOOLEAN,
    non_native_introduced BOOLEAN,
    non_native_invasive BOOLEAN,
    genera_id INTEGER REFERENCES genera (genera_id),
    family_id INTEGER REFERENCES family (family_id),
    phyla_id INTEGER REFERENCES phyla (phyla_id)
);

CREATE TABLE plants.counties
(
    county_id SERIAL UNIQUE NOT NULL PRIMARY KEY,
    county_name VARCHAR(50) NOT NULL
);

-- table checks for species occurance in a county
CREATE TABLE plants.county_occurance
(
    species_id INTEGER REFERENCES species (species_id),
    county_id INTEGER REFERENCES counties (county_id)
);
;