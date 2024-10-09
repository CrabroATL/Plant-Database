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
3. create docker container

### Prerequisites
Enumerated prerequisites.

1. Python 3 installed
    #### Required Packages
    1. pytesseract            0.3.10
    2. psycopg2-binary        2.9.9
    3. pillow                 10.3.0
    4. numpy                  1.26.4
    5. matplotlib             3.9.0
2. Postgres SQL installed
3. Golang V 1.21.0 installed
4. Docker v 4.34.2 installed

### Installation

#### Step 1: Create Docker Container
First create a docker container. Ensure your container information matches the database connection string
dbname=postgres user=postgres password=password host=0.0.0.0 port=30420

#### Step 2: Build Database
Next run migrations.py to build the pgsql database.

#### Step 3: Populate Database
Next run data_extractor.py to populate database. This process current takes between 640s and 660s 

#### Step 4: Clean Data
Next run edgecase_cleaner.py to clean all currently known ocr errors.

#### Step 5: Run WebApp
Last run main.go to host a local server for the webapp. Then search for the plants you've always wanted to know about!

## Testing

### Unit Tests
Describe how unit tests are executed.

### Integration Tests

Describe how integration tests are executed.

## Deployment

Explain how the app or library is deployed or executed either in a local or server context.

## Technology Stack

1. pgsql
2. Python3
3. GoLang
4. Docker
5. 