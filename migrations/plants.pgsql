
DROP SCHEMA AR_PLANTS CASCADE;

CREATE SCHEMA ar_plants;

SET search_path TO ar_plants;

CREATE TABLE ar_plants.phyla
(
    phyla_id SERIAL UNIQUE NOT NULL PRIMARY KEY,
    polyphylactic_group VARCHAR(50) NOT NULL
);

INSERT INTO ar_plants.phyla (polyphylactic_group) VALUES
    ('pteridophytes'),
    ('gymnosperms'), 
    ('angiosperm dicots'), 
    ('angiosperm monocots')
;

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
    scientific_name VARCHAR NOT NULL,
    common_name VARCHAR NOT NULL,
    native BOOLEAN,
    endemic BOOLEAN,
    special_concern BOOLEAN,
    introduced BOOLEAN,
    invasive BOOLEAN,
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

INSERT INTO ar_plants.counties (county_name) VALUES
    ('arkansas'),
    ('ashley'),
    ('baxter'),
    ('benton'),
    ('boone'),
    ('bardley'),
    ('calhoun'),
    ('carroll'),
    ('chicot'),
    ('clark'),
    ('clay'),
    ('cleburne'),
    ('cleveland'),
    ('columbia'),
    ('conway'),
    ('craighead'),
    ('crawford'),
    ('crittenden'),
    ('cross'),
    ('dallas'),
    ('desha'),
    ('drew'),
    ('faulkner'),
    ('franklin'),
    ('fulton'),
    ('garland'),
    ('grant'),
    ('greene'),
    ('hempstead'),
    ('hotspring'),
    ('howard'),
    ('independence'),
    ('izard'),
    ('jackson'),
    ('jefferson'),
    ('johnson'),
    ('lafayette'),
    ('lawrence'),
    ('lee'),
    ('lincoln'),
    ('littleriver'),
    ('logan'),
    ('lonoke'),
    ('madison'),
    ('marion'),
    ('miller'),
    ('mississippi'),
    ('monroe'),
    ('montgomery'),
    ('nevada'),
    ('newton'),
    ('ouachita'),
    ('perry'),
    ('phillips'),
    ('pike'),
    ('poinsett'),
    ('polk'),
    ('pope'),
    ('prairie'),
    ('pulaski'),
    ('randolph'),
    ('saintfrancis'),
    ('saline'),
    ('scott'),
    ('searcy'),
    ('sebastian'),
    ('sevier'),
    ('sharp'),
    ('stone'),
    ('union'),
    ('vanburen'),
    ('washington'),
    ('white'),
    ('woodruff'),
    ('yell')
;
