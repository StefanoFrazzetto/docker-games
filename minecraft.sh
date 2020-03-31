#!/usr/bin/env bash

# Handle command failures by exiting and print the error cause
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

# Server variables
s3_bucket="<YOUR_MINECRAFT_BUCKET_NAME>"
server_data="$HOME/minecraft-data"
server_memory="1500M"
server_port=25565

# Check data directory
if [ ! -d "$server_data" ]; then
    mkdir "$server_data"
fi

# Mount S3 bucket
s3fs "$s3_bucket" "$server_data" -o allow_other

# Start Minecraft
docker run -d -it \
	--mount type=bind,src="$server_data",target=/data \
	-e EULA=TRUE \
	-e MEMORY="$server_memory" \
	-p $server_port:25565 \
	--name minecraft \
	itzg/minecraft-server

