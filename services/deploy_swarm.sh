#! /bin/bash

export $(cat ../.env) > /dev/null 2>&1
docker stack deploy -c meilisearch/deploy.yml -c postgres/deploy.yml fm_services
 
