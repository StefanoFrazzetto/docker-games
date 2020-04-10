#!/usr/bin/env bash

source functions.sh

# Check data directory
if [ ! -d "$minecraft_local_data" ]; then
    mkdir "$minecraft_local_data"
fi

# Mount S3 bucket
s3fs "$minecraft_s3_bucket" "$minecraft_local_data" -o allow_other

# Start Minecraft
docker run -d -it \
	--mount type=bind,src="$minecraft_server_data",target=/data \
	-e EULA=TRUE \
	-e MEMORY="$minecraft_server_memory" \
	-e ONLINE_MODE="$minecraft_server_online_mode" \
	-p $minecraft_server_port:25565 \
	--name minecraft \
	itzg/minecraft-server

