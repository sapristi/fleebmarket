#! /bin/bash

set -x
source $VENV_PATH/bin/activate
cd $EXEC_PATH
uwsgi config/uwsgi.ini
