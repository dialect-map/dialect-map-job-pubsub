#!/usr/bin/env sh

# The script exits when a command fails or it uses undeclared variables
set -o errexit
set -o nounset


copies_dir="old"
parent_dir=".update"

# Argument parsing
while [ "$#" -gt 0 ]; do
    case $1 in
        -c|--copies_dir) copies_dir="$2";       shift  ;;
        -p|--parent_dir) parent_dir="$2";       shift  ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done


PROJECT_DIR="$(dirname "$0")/.."

DATA_MODULE_PATH="${PROJECT_DIR}/modules/dialect-map-data/data"
DATA_COPIES_PATH="${PROJECT_DIR}/${parent_dir}/${copies_dir}"


# Create the copies directory
mkdir -p "${DATA_COPIES_PATH}"

# Move the current data files there
cp -r "${DATA_MODULE_PATH}/." "${DATA_COPIES_PATH}"
