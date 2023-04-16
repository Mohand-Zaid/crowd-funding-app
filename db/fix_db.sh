#!/bin/bash

if [ -f "./db/users.json" ]
then
    cp "./db/users.json" "./db/users.bk"
    rm "./db/users.json"
    mv  "./db/users.bk" "./db/users.json"
    echo "users.json : fixed"

elif [ ! -f "./db/users.json" ]
then
    touch "./db/users.json"
    echo "new users.json added"
fi

if [ -f "./db/projects.json" ]
then
    cp "./db/projects.json" "./db/projects.bk"
    rm "./db/projects.json"
    mv "./db/projects.bk" "./db/projects.json"
    echo "projects.json : fixed"

elif [ ! -f "projects.json" ]
then
    touch "./db/projects.json"
    echo "new projects.json added"
fi
