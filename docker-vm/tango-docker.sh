#!/bin/bash
LOCALIP=$(ip route get 1 | awk '{print $NF;exit}')

echo "LOCAL IP address " $LOCALIP

if [ $# == 2 ]; then
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
    echo "tango-db image compiled"
else
    echo "tango-db image exists"
fi

docker run -d -e MYSQL_ROOT_PASSWORD=root -p $mysql_port:3306 --name tango-db tango-db 2>&1 | grep 'Conflict. The name'
if [[ $? -eq 0 ]]; then
    echo "Restarting tango-db"
    docker restart tango-db
fi

if [[ "$(docker images -q tango-core 2> /dev/null)" == "" ]]; then
    # if the image doesn't exists
    echo "tango-core image doesn't exists"
    git clone https://github.com/tango-controls/tango-cs-docker.git
    docker build -t tango-core ./tango-cs-docker/
    echo "tango-core image compiled"
else
    echo "tango-core image exists"
fi


# tango-core è il nome del container che vado a creare, MYSQL_HOST punta al database MySQL e l'ultimo tango è l'immagina docker
docker run -d --name tango-core -p $tango_port:10000 -e ORB_PORT=10000 -e TANGO_HOST=$LOCALIP:10000 -e MYSQL_HOST=$LOCALIP:$mysql_port -e MYSQL_USER=tango -e MYSQL_PASSWORD=tango -e MYSQL_DATABASE=tango tango-core 2>&1 | grep 'Conflict. The name'
if [[ $? -eq 0 ]]; then
    echo "Restarting tango-core"
    docker restart tango-core
fi
