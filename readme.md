# Arkansas Vascular Plants Searchable Database

## Description
This app takes the online pdf version of "Atlas of the Vascular Plants of Arkansas" and creates a searchable database based on location, taxonomic, and native status. This data from the pdf is extracted using OCR and bitmapping to collect text and map data, cleaned and uploaded into a Postgres database. That database is accessed by a webapp that allows users to search based on county presence and taxonomic data. 
This streamlines the searching process, and allows more granular and focused searches to be done, especially when it comes to location. Previously location data was exclusively gathered by looking at a map of the state of Arkansas with a dot in each county the plant is present. Any cross referncing must be done manually. 
As a native plant enthusiate, I regulary used the Atlas of Vascular Plants of Arkansas to select plants, searching for what plants were native to my county, or checking if a plant I was trying to purchase was native, or occured in my county was a tedious chore. This database sovles that issues and turns a 10-20 minute process into a 4-5 second process. There are also possible use cases in conservation work and botany research, allowing for quick mapping based family and genus.  

## Getting Started
Description of steps to get local development environment set up.
1. Copy github repo
2. install prereqs
3. create docker container

### Prerequisites
Enumerated prerequisites.

1. Python 3 installed
2. Postgres SQL installed
3. Golang V 1.21.0 installed
4. Docker v 4.34.2 installed

### Installation
Description of how the app or library is built.

## Testing

### Unit Tests
Describe how unit tests are executed.

### Integration Tests

Describe how integration tests are executed.

## Deployment

Explain how the app or library is deployed or executed either in a local or server context.

## Technology Stack

Enumerated list of language and frameworks used for this project.