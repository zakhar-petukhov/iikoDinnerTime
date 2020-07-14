#!/usr/bin/env bash

echo Updating git repo...
git pull git@github.com:zakhar-petukhov/DinnerTime.git

echo Updating images...
if [[ $1 ]]
then
    cd ..

    path=`pwd`
    proj=`basename $path`

    export $(grep -v '^#' prod.env | xargs)

    docker login -u="korolevich" -p=${DOCKER_TOKEN}

    docker build -f Dockerfile -t korolevich/dinner_time:$1 .

    docker push korolevich/dinner_time:$1

    echo Built and pushed $proj:$1

else
    echo Specify version number
fi


