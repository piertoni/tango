#!/bin/bash
# Get ip
LOCALIP=$(ip route get 1 | awk '{print $NF;exit}')

echo "LOCAL IP address " $LOCALIP
if [ $# == 2 ]
    then
	mysql_port=$1
	echo "MYSQL PORT $1"
	tango_port=$2
	echo "TANGO PORT $2"
else
    echo "MYSQL Standard Port 3306"
    echo "Tango Standard Port 10000"
    echo "Usage:"
    echo "tango-docker.sh MYSQLPORT TANGO_PORT"
    exit
fi

if [[ "$(docker images -q tango-db 2> /dev/null)" == "" ]]; then
    # if the image doesn't exists
    echo "tango-db image doesn't exists"
    git clone https://github.com/tango-controls/docker-mysql.git 

    #  Compilazione
    docker build -t tango-db ./docker-mysql/
fi
    echo "tango-db image exists"

if [[ "$(docker images -q tango-core 2> /dev/null)" == "" ]]; then
    # if the image doesn't exists
    echo "tango image doesn't exists"
    git clone https://github.com/tango-controls/tango-cs-docker.git
    docker build -t tango-core ./tango-cs-docker/
fi
    echo "tango image exists"

docker run -d -e MYSQL_ROOT_PASSWORD=root -p 13306:3306 --name tango-db tango-db 2>&1 | grep 'Conflict. The name'
if [[ $? -eq 0 ]]
    then
    echo "Container tango-db already exists, restarting..."
    docker restart tango-db
fi

# tango-core è il nome del container che vado a creare, MYSQL_HOST punta al database MySQL e l'ultimo tango è l'immagina docker
docker run -d --name tango-core -p 10000:10000 -e ORB_PORT=10000 -e TANGO_HOST=$LOCALIP:10000 -e MYSQL_HOST=$LOCALIP:13306 -e MYSQL_USER=tango -e MYSQL_PASSWORD=tango -e MYSQL_DATABASE=tango tango-core 2>&1 | grep 'Conflict. The name'
if [[ $? -eq 0 ]]
then
    echo "Container tango-core already exists, restarting..."
    docker restart tango-core
fi

