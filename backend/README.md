# DEV Installation

The usage of a virtualenv is recommanded.
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Copy `.env.skeleton` to `.env` and fill in the values. Set `APP_ENV=dev` in the `fleebmarket_django` env file.


## Setup

Setup the db: after activating the virtualenv, run
```
python manage.py migrate
```

See the readme in `meilisearch_front` project to setup javascript static files.


## Run

To run dev app: (serves both django and fastapi, with `DEBUG=true` to serve static files, although this might be superflous with `whitenoise`):

```
DEBUG=true uvicon fleebmarket.asgi:app --reload
```

## Run tests

Install `requirements-dev.txt`
Run `pytest` from the `fleebmarket_django` folder.

# Create account provider apps

 * Reddit: https://www.reddit.com/prefs/apps/
 * discord: https://discord.com/developers/applications
 
and set related field in `.env` file. This is usefull if you want to develop features related to those kind of accounts; otherwise you can log in the django admin panel at `localhost:8000/admin`, and then go back to the website.
