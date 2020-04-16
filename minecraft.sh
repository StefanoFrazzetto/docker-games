#!/usr/bin/env bash

source functions.sh

# Start Minecraft
docker run -d -it \
	--mount type=bind,src="$minecraft_local_data",target=/data \
	-e EULA=TRUE \
	-e MEMORY="$minecraft_server_memory" \
	-e ONLINE_MODE="$minecraft_server_online_mode" \
	-p $minecraft_server_port:25565 \
	--name minecraft \
	itzg/minecraft-server

