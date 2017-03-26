#!/bin/bash
if [ $# == 2 ]
    then
	mysql_port=$1
	echo "MYSQL PORT $1"
	tango_port=$2
	echo "TANGO PORT $2"
else
    echo "Starting MYSQL on localhost on Standard Port 3306"
    echo "Starting Tango on localhost on Standard Port 10000"
    echo "Usage:"
    echo "tango-docker.sh MYSQLPORT TANGO_PORT"
fi

if [[ "$(docker images -q tango-db 2> /dev/null)" == "" ]]; then
    # if the image doesn't exists
    echo "tango-db image doesn't exists"
    git clone https://github.com/tango-controls/docker-mysql.git 

    #  Compilazione
    docker build -t tango-db ./docker-mysql/
fi
    echo "tango-db image exists"

if [[ "$(docker images -q tango_databaseds 2> /dev/null)" == "" ]]; then
    # if the image doesn't exists
    echo "tango image doesn't exists"
    git clone https://github.com/tango-controls/tango-cs-docker.git
    docker build -t tango_databaseds ./tango-cs-docker/
fi
    echo "tango image exists"

docker run -d -e MYSQL_ROOT_PASSWORD=root -p 13306:3306 --name tango-db tango-db 2>&1 | grep 'Conflict. The name'
if [[ $? -eq 0 ]]
    then
    echo "Container tango-db already exists, restarting..."
    docker restart tango-db
fi

# tango_databaseds è il nome del container che vado a creare, MYSQL_HOST punta al database MySQL e l'ultimo tango è l'immagina docker
docker run -d --name tango_databaseds -p 10000:10000 -e ORB_PORT=10000 -e TANGO_HOST=localhost:10000 -e MYSQL_HOST=localhost:13306 -e MYSQL_USER=tango -e MYSQL_PASSWORD=tango -e MYSQL_DATABASE=tango tango_databaseds 2>&1 | grep 'Conflict. The name'
if [[ $? -eq 0 ]]
then
    echo "Container tango_databaseds already exists, restarting..."
    docker restart tango_databaseds
fi

