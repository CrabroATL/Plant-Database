# Arkansas Vascular Plants Searchable Database

## Description
This app takes the online pdf version of "Atlas of the Vascular Plants of Arkansas" and creates a searchable database based on location, taxonomic, and native status. As a native plant enthusiate, I regulary used the Atlas of Vascular Plants of Arkansas to select plants, searching for what plants were native to my county, or checking if a plant I was trying to purchase was native, and if it occured in my county was a tedious chore. This database sovles that issues and turns a 10-20 minute process into a 4-5 second process. There are also possible use cases in conservation work and botany research, allowing for quick location mapping based family and genus.  

## Components

### Data Extractor
The data from the pdf is extracted using Python3, with OCR and bitmapping libraries to collect text and map data. It is then cleaned and uploaded into a Postgres database running in Docker. 

### WebApp
That database is accessed by a webapp built in GoLang that allows users to search based on county presence and taxonomic data. This streamlines the searching process, and allows more granular and focused searches to be done, especially when it comes to location. Previously location data was exclusively gathered by looking at a map of the state of Arkansas with a dot in each county the plant is present. Any cross referncing was done manually. 

## Getting Started
Description of steps to get local development environment set up.
1. Copy github repo
2. install prereqs

### Prerequisites
Enumerated prerequisites.

1. Python 3 installed
    #### Required Packages
    1. pytesseract            0.3.10
    2. psycopg2-binary        2.9.9
    3. pillow                 10.3.0
    4. numpy                  1.26.4
    5. matplotlib             3.9.0
    6. imageio                2.34.1
2. Postgres SQL installed
3. Golang V 1.21.0 installed
4. Docker v 4.34.2 installed

### Installation

#### Step 1: Build Docker Container & Database
Run the following commands in the command while inside the plant_database directory

    docker build -t plant-db -f Dockerfile.DB .
    docker run -d -p 8001:5432 plant-db

#### Step 2: Populate Database
Next, run data_ELT.py to populate database. This process current takes between 640s and 660s 

#### Step 3: Build and Run WebApp
Last, execute the following commands

docker build -t plant-server -f Dockerfile.Server ./
docker run -p 8080:8080 plant-server

## Testing

### Unit Tests

Using quicktest.py known locations of counties in a selected image can be verfied to have been read correctly. 
Programs generacheck.py and family_check.py were used to find errors in the OCR that needed to be fixed with the edgecase cleaner.

Future go tests will be implemented later.

### Integration Tests

No integration tests were run.

## Deployment

The app is run on local port 8080 and accessed through a web browser. Future versions target being hosted on a webserver.

## Technology Stack

1. pgsql
2. Python3
3. Javascript
4. GoLang
5. Docker

## Known and Possible Bugs

1. Database connection string may break on some machines. This issue is being looked into

## Improvements in development

1. Harden database and query logic to prevent SQL injection attacks.
2. Use Docker Compose to network containers
3. Secondary python program to pull additional Taxa data from source material.