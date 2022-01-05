# Scrapper

The scrapper is responsible for fetching new posts appearing on `/r/mechmarket`, and updating posts already in databse.

## Setup

In a virtualenv, install the dependencies: `pip install -r requirements.txt`.

## Run

Go to this project root dir.

Show options:
```
python -m scrapper --help
```

Example command to run in order to test/develop:
```
python -m scrapper --dotenv ../.env --update-batch-size 10 --max-last-submissions 10 --debug
```
 
