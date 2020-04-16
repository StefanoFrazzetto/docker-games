#!/usr/bin/env bash

source functions.sh

# Start server
docker run --name teamspeak \
       -p 9987:9987/udp -p 10011:10011 -p 30033:30033 \
       -v "$teamspeak_local_data":/var/ts3server/
       -e TS3SERVER_LICENSE=accept teamspeak
