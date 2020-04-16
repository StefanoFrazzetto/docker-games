#!/usr/bin/env bash

# Handle command failures by exiting and print the error cause
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' ERR

# Prompt the user for confirmation
function ask_for_confirmation {
    echo -e "\n"
    while true; do
    read -p "Do you want to proceed? (y/n): " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
    done
    echo -e "\n"
}

# Parse a yaml configuration file
function parse_yaml {
   local prefix=$2
   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
   sed -ne "s|^\($s\):|\1|" \
        -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  $1 |
   awk -F$fs '{
      indent = length($1)/2;
      vname[indent] = $2;
      for (i in vname) {if (i > indent) {delete vname[i]}}
      if (length($3) > 0) {
         vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
         printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
      }
   }'
}

# Get the script name via reference
function get_script_name {
    filename=$(basename -- "$0")
    extension="${filename##*.}"
    filename="${filename%.*}"
    eval "$1=$filename"
}

# Print the caller script name
function print_script_name {
    # Get value by reference 
    get_script_name script_name
    figlet -f small "$script_name"
    echo -e "\n"
}

# Check if we're on an AWS instance
# Source: https://serverfault.com/a/700771
function is_aws_instance {
    if [ -f /sys/hypervisor/uuid ] && [ `head -c 3 /sys/hypervisor/uuid` == ec2 ]; then
        return 0 # true
    else
        return 1 # false
    fi
}

# Print a nice banner
print_script_name

# Load configuration from the yaml file
eval $(parse_yaml config.yaml)

# Use the script name to create the variables name
data_dir="${script_name}_local_data"
s3_bucket="${script_name}_s3_bucket"

# Get the values by expansion
echo "Saving local data to ${!data_dir}"

# Check empty or missing S3 bucket variable
if [ -z "${!s3_bucket}" ]; then
    echo "S3 bucket not set. Your data will be saved locally, so make sure to create a backup!"
    ask_for_confirmation
else
    echo "The data will be stored into the following S3 bucket: s3://${!s3_bucket}"
    
    ask_for_confirmation

    # Finally mount the bucket
    # TODO: Check if this is necessary
    if is_aws_instance; then
        s3fs "$minecraft_s3_bucket" "$minecraft_local_data" -o iam_role=auto -o allow_other
    else
        s3fs "$minecraft_s3_bucket" "$minecraft_local_data" -o allow_other
    fi
fi

# Check if data directory
if [ ! -d "${!data_dir}" ]; then
    mkdir "${!data_dir}"
fi