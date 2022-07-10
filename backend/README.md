# Presentation

This folder contains all the backend code for fleebmarket. 

# DEV Installation

The usage of a virtualenv is recommanded.
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Main commands

- Run web server:  
  `uvicon fleebmarket.asgi:app --reload`
- Run tests:  
  `pytest`

## Management commands

A number of management commands are provided. Run `./manage.py COMMAND --help` for help and subcommands.

- `[fleebmarket]`
  - `alerts`: Collect alerts from journald and services status.
  - `debug_db`: Help debug db.
  - `meilisearch`: Manage meilisearch.
  - `monitor`: Help monitor meilisearch.
  - `services`: Manage Blue/Green services
  - `update_frontend`: Build frontend, and update django static files.

- `[search_app]`
  - `db_status`: Print some stats on the db (debug).
  - `mark_duplicates`: Mark duplicate adds (usefull when duplicate algorithm changes).
  - `parse_again`: Parse adverts again, and populate advert items anew.
   

# Django apps

The following django apps are in the project:
- `accounts`: custom accounts (user model and such).
- `advert_parsing`: code use to extract items from adverts (not a django-app per se).
- `alerts`: send alerts to user when an advert matches the given criteria.
- `fleebmarket`: contains settings, and common code.
- `scrapper`: scrap posts on `/r/mechmarket`.
- `search_app`: interacts with the frontend for the search.
- `survey`: can be used to make surveys.

