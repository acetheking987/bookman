#!/bin/bash

# Build the docker image
echo "Building the docker image"
docker build -t bookman .

# Run the docker image
echo "Running the docker compose"
sudo docker-compose up -d --remove-orphans