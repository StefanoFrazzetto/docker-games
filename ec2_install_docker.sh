#!/usr/bin/env bash

# Handle command failures by exiting and print the error cause
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

# Check user is root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user
