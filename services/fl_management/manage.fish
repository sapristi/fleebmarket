#! /usr/bin/fish

set -x DBUS_SESSION_BUS_ADDRESS unix:path=/run/user/(id -u)/bus
set -x XDG_RUNTIME_DIR /run/user/(id -u)

set current (status --current-filename)

if [ -L $current ]
   set current (readlink $current)
end

set workdir (dirname $current)
cd $workdir

source .venv/bin/activate.fish

python -m manage $argv
