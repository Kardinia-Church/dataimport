# Kardinia Church Modifications
This project contains extra files for managing our specific import requirements.

## Seperate CSV
Separates a CSV file into smaller files

## Convert Notes
Converts notes exported from Elvanto into a useable format

## Convert Service Attendance
Converts individual service attendance exported from Elvanto's inbuilt ```Service Individual Attendance``` function into the correct format to be imported
### To export
1. Goto services/reports
2. Export the ```Service Individual Attendance``` with the following ticked
    * Member ID
    * Full Name
    * First Name
    * Last Name
    * Gender
    * Date of Birth

A file ```services.csv``` will also be generated this keeps track of the randomly assigned ids for each service found allowing for separation of exports. This should be deleted if a new import is being run

The converted file will be outputted using append mode, this will append new records if the file exists

# Elvanto to Flurio Data Importer
This project is forked from [fluro-developers/dataimport](https://github.com/fluro-developers/dataimport) with modifications for our specific import requirements

# Data Import 
Requires NodeJS 

# Installation

```
git clone git@github.com:fluro-developers/dataimport.git
```
```
cd dataimport
```
```
npm install

```


# Adding your files
Add any CSV documents you want to import into the /files folder, then run the script

# Run
```
node index.js
```


# Data Mapping
Adjust Column Names for your CSVs by editing the index.js document before running the script.

### How it works
This script will first prompt you to login, then ask you to select:
- An account
- A default realm
- The file you wish to import
- The kind of import (3 options, Attendance checkins, Headcount Numbers or Contact Notes)

Once you have started the import, it will sequentially iterate through each of the rows and run a check to see if the row has already been imported in to your account,
if it has not been imported yet it will then create it and continue. This means it is safe to import the same document multiple times without creating duplicate records.
If you see your terminal printing 404 connection issues, this is standard and actually a good thing, it's telling you that the document does not exist and it will try and create it