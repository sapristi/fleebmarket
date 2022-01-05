# Fleebmarket

This repo holds configuration files for services used by fleebmarket, and the other fleebmarket repos as git submodules.

## Local setup

1. Clone this repo, then run `git submodule update --init`.
2. Copy `.env.skeleton` to `.env`, then fill the values.
3. Start a postgres and meilisearch instance as docker containers by running `scripts/deploy_swarm.sh`.
4. Setup the client: 
    1. Create a symlink from `fleebmarket_django/fleebmarket_django/search_app/static/search_app` to `meilisearch_front/build/static`.
    2. Move to `meilisearch_client` directory and run
       - `yarn install`
       - `yarn build`
5. Setup the backend:
   1. Go to the `fleebmarket_django` directory, then follow the readme there
   2. Run `python manage.py collectstatic`.
   3. Run the server
6. Setup the scrapper
   
Once the scrapper starts to run, the db should be populating with latests posts on /r/mechmarket.


### Access services

In order to access the db, run `psql fleebmarket -U postgres`

## Server inventory

### Files and folders

#### Programs

Two folders for B/G deployment:

 - `/fleebmarket_blue`: blue instance (backend, scrapper)
 - `/fleebmarket_green`: green instance (backend, scrapper); to come

Old instance: 
 - `/fleebmarket`

#### Data

Data, in the `/data` folder:
 - `backups`: db backups.
 - `fleebmarket_{blue,green}`: django data for B/G instances (if we were to use django `media`, this would be an issue; only `static` for now).
 - `meilisearch`: meilisearch database files.
 - `postgres` : postgres db files.
 - `fleebmarket`: legacy fleebmarket django data.

### Services

#### Fleebmarket

Two services are running for the backend: `backend@blue` and `backend@green`.
For the cronjobs, a single service should be running at any time ( either `cronjobs@blue` or `cronjobs@green`).

Example commands:
| Command                                                 | Description                                                                                                               |
|---------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Get service status                                      | `systemctl --user status backend@blue`                                                                                    |
| Restart a service                                       | `systemctl --user restart backend@blue`                                                                                   |
| Get logs                                                | `journalctl --user-unit backend@blue.service -f`                                                                          |
| Combine logs for both services, filter `scrapper` lines | `journalctl --user-unit -u backend@blue -u backend@green -f --since "2021-10-26 16:00" \| lnav -c ":filter-out scrapper"` |

#### Databases

Both databases (postgres and meilisearch) are running as docker services. For now they are not accessible to the `flu` user (if the need arises, I might go for a "rootless docker" setup, as described [here](https://docs.docker.com/engine/security/rootless/); seems unlikely, services have been running without issue for months ).

#### Monitoring

Two monitoring services are running on the server. To access those services, you should have configured your ssh connection as described in the first part, and have an ssh session running.

- monitorix, used for long time monitoring. You can access the service at `http://localhost:7777/monitorix`.
- netdata, for short term monitoring. You can access the service at `http://localhost:19999`.

### Blue / Green deployment

Two backend services are running at any time:
 - the **main** one is tied to https://fleebmarket.mmill.eu 
 - the **aux** one is tied to https://fleebmarket.mmill.eu:444


When you are ready to merge a new feature, checkout you branch in the folder corresponding to the current **aux** instance, then restart the corresponding service. You can then see the result at https://fleebmarket.mmill.eu:444.
Once the feature is merged, checkout the tag/develop branch in the **aux** instance, then run `sudo /fleebmarket_blue/services/swap.sh`. This will swap the **aux** and **main** instances, without disrupting current requests.
