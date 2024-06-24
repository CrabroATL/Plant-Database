-- Create a new table called 'TableName' in schema 'SchemaName'
-- Drop the table if it already exists
CREATE DATABASE plants;

CREATE SCHEMA ar_plants;

SET search_path TO ar_plants;

CREATE TABLE ar_plants.phyla
(
    phyla_id SERIAL UNIQUE NOT NULL PRIMARY KEY,
    polyphylactic_group VARCHAR(50) NOT NULL
);

CREATE TABLE ar_plants.family
(
    family_id SERIAL UNIQUE NOT NULL PRIMARY KEY,
    family VARCHAR(50) NOT NULL,
    phyla_id INTEGER REFERENCES phyla (phyla_id)
);

CREATE TABLE ar_plants.genera
(
    genera_id SERIAL UNIQUE NOT NULL PRIMARY KEY,
    genera VARCHAR(50) NOT NULL,
    family_id INTEGER REFERENCES family (family_id),
    phyla_id INTEGER REFERENCES phyla (phyla_id)
);

CREATE TABLE ar_plants.species
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

CREATE TABLE ar_plants.counties
(
    county_id SERIAL UNIQUE NOT NULL PRIMARY KEY,
    county_name VARCHAR(50) NOT NULL
);

CREATE TABLE ar_plants.county_occurance
(
    species_id INTEGER REFERENCES species (species_id),
    county_id INTEGER REFERENCES counties (county_id)
);
