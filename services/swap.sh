#! /bin/bash

cd /etc/nginx/conf-bg

if [ "$(readlink main)" = "blue" ]
then
    echo "Main instance is blue; swapping"
    rm -f main
    rm -f aux
    ln -s blue aux
    ln -s green main
    nginx -s reload
    echo "Main instance is now green"
else
    echo "Main instance is green; swapping"
    rm -f main
    rm -f aux
    ln -s green aux
    ln -s blue main
    nginx -s reload
    echo "Main instance is now blue"
fi
