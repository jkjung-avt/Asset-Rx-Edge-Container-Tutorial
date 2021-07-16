#!/bin/bash
Help()
{
    echo "This go.sh gets your AssetRxEdge Microservices built and ready to GO!"
    echo
    echo "Syntax: ./go.sh [build|push|run]"
    echo "arguments:"
    echo "  build     Builds the amd64 and arm64/v8 Microservice docker images. Then pushes."
    echo "  push      Pushes your latest built images.    #Dont forget to build first!#"
    echo "  run       Runs a local version of your docker container for testing with docker args:"
    echo "              -v\$PWD/app:/app -p8080:8080 "
    echo
}

if [ "$#" -ne 1 ]; then
    Help
    exit 1
fi
image_name=${PWD##*/}
# user_name="cratustech"
user_name="jkjung13"

if [ $1 == "build" ]; then
    # sudo docker buildx build --platform linux/amd64,linux/arm64/v8 -t $user_name/$image_name:latest --push .
    sudo docker buildx build --platform linux/arm64/v8 -t $user_name/$image_name:latest --push .
elif [ $1 == "push" ]; then
    sudo docker push $user_name/$image_name:latest
elif [ $1 == "run" ]; then
    sudo docker run --rm --name $image_name-inst -p8080:8080 $user_name/$image_name:latest
    # sudo docker run --rm --name $image_name-inst -v$PWD/app:/app -p8080:8080 cratustech/$image_name:latest
fi
