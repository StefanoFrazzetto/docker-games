#!/usr/bin/env bash

# Handle command failures by exiting and print the error cause
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' ERR

# Check for 'y' or 'yes', otherwise unset the trap and exit
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
    #read -p "Do you want to proceed? (y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || trap - EXIT && echo "Exiting..." && exit 1
}

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

# Get the script name
function get_script_name {
    filename=$(basename -- "$0")
    extension="${filename##*.}"
    filename="${filename%.*}"
    eval "$1=$filename"
}

# Print the script name
function print_script_name {
    # Get value by reference 
    get_script_name script_name
    figlet -f small "$script_name"
    echo -e "\n"
}

# Print a nice banner
print_script_name

# Load configuration from the yaml file
eval $(parse_yaml config.yaml)

# Use the script name to create the variables name
data_dir="${script_name}_local_data"
s3_bucket="${script_name}_s3_bucket"

# Get the variables' values by expansion
echo "Saving local data to ${!data_dir}"
echo "The data will be stored into the following S3 bucket: s3://${!s3_bucket}"

ask_for_confirmation
