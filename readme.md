# Fleebmarket

Fleebmarket is a frontend to the [/r/mechmarket](https://reddit.com/r/mechmarket) subreddit (seconds hand mechanical keyboards marketplace). You can reach the website at "https://fleebmarket.mmill.eu"

This repo holds the full source code of the  website.

# Tech stack

- Python/Django for the backend (+ Uvicorn/nginx for lower level request handling)
- [Huey](https://github.com/coleifer/huey) for periodic tasks
- Postgresql for the django database
- [Meilisearch](https://github.com/meilisearch/meilisearch) for the search database
- JavaScript/React/[Bulma](https://bulma.io/) for the frontend

# Local setup

1. Copy `.env.skeleton` to `.env`, then fill the values (you can ignore settings for blue/green deployment)
2. Start a postgres and meilisearch instance as docker containers by running `scripts/deploy_swarm.sh`.
3. Setup the [backend](./backend)
   
# Prod setup

Fleebmarket is currently deployed on a bare-metal server, this sections describe the current setup.

It shouldn't be too difficult to adapt, or even dockerize everything, but some settings are hard-coded.

## Files

- This repository is cloned in two folders, `/fleebmarket_blue` and `/fleebmarket_green`. 
- `.env` files, with values for blue/green deployment set-up accordingly.
- A python virtualenv is set in `backend/.venv` for each of these folders.
- A `/data` folder contains data for the various services. It contains the following folders (some have to be manually created):
  - `alerts`: alerts configuration
  - `backend_blue`, `backend_green`: django static files for each of the backends
  - `huey`: huey database
  - `meilisearch`: meilisearch database
  - `postgres`: postgres database

## Systemd services

Services are run as systemd user services. Services files are present in the [`services/systemd`](services/systemd) directory, which is symlinked on the server to `~/.config/systemd/user`. Services can then be managed with `systemd --user` commands:

- `meilisearch.service` and `postgresql.service` can be enabled and started right away
- The services for the backend and cronjobs have to be declined for Blue and Green instances:
  - `backend@blue.service`, `backend@green.service`
  - `cronjobs@blue.service`, `cronjobs@green.service`

The alerting system works by parsing journald logs.

## Nginx

Nginx is the only service running as root. You can find configuration files in [`services/nginx`](services/nginx).

## Monitoring

Monitorix is used to monitor the server, as well as fleebmarket usage. Some settings can be found in [`services/monitorix`](services/monitorix).

Additionally, a Huey job parses journald logs, and send alerts to the configured discord channel when it finds messages with level ERROR or higher ([cysystemd](https://github.com/mosquito/cysystemd) is used to give the right level to python log messages).


# Create account provider apps

 * Reddit: https://www.reddit.com/prefs/apps/
 * discord: https://discord.com/developers/applications
 
and set related field in `.env` file. This is usefull if you want to develop features related to those kind of accounts; otherwise you can log in the django admin panel at `localhost:8000/admin`, and then go back to the website.
