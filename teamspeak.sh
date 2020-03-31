#!/usr/bin/env bash

# Handle command failures by exiting and print the error cause
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

s3_bucket="<YOUR_TEAMSPEAK_BUCKET_NAME>"
server_data="$HOME/teamspeak-data"

# Check data directory
if [ ! -d "$server_data" ]; then
    mkdir "$server_data"
fi

# Mount S3 bucket
s3fs "$s3_bucket" "$server_data" -o allow_other

# Start server
docker run --name teamspeak \
       -p 9987:9987/udp -p 10011:10011 -p 30033:30033 \
       -v "$server_data":/var/ts3server/
       -e TS3SERVER_LICENSE=accept teamspeak

