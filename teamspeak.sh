#!/usr/bin/env bash

source functions.sh

# Check data directory
if [ ! -d "$teamspeak_server_data" ]; then
    mkdir "$teamspeak_server_data"
fi

# Mount S3 bucket
s3fs "$teamspeak_s3_bucket" "$teamspeak_server_data" -o allow_other

# Start server
docker run --name teamspeak \
       -p 9987:9987/udp -p 10011:10011 -p 30033:30033 \
       -v "$teamspeak_server_data":/var/ts3server/
       -e TS3SERVER_LICENSE=accept teamspeak

