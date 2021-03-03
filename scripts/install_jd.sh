#!/usr/bin/env sh

# The script exits when a command fails or it uses undeclared variables
set -o errexit
set -o nounset


# Get the OS name
SYSTEM_TYPE=$(uname)


if [ "${SYSTEM_TYPE}" = "Linux" ]; then
    printf "Installing on Linux\n"
    apt update
    apt install golang-go
    export PATH=~/go/bin:$PATH
    export GO111MODULE=on
    go get "github.com/josephburnett/jd@v1.3.0"

elif [ "${SYSTEM_TYPE}" = "Darwin" ]; then
    printf "Installing on Mac OS\n"
    brew install jd

else
    printf "Unsupported OS\n"
    exit 1
fi
