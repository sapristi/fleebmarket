#! /usr/bin/env fish

echo "STARTING SCRAPPER SERVICE"

set workdir (dirname (status --current-filename))
cd $workdir
source .venv/bin/activate.fish

python -m scrapper loop --journald-logs Cronjobs[$INSTANCE_NAME]
