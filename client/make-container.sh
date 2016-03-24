#!/bin/bash

# this needs to move to the container. but rhino sucks...

rm -rf ./Docker/app
rm -rf ./Docker/cappuccino
rm -rf ./Docker/narwhal

# export CAPP_BUILD="$(pwd)/Docker/cappuccino"
# export CAPP_INSTALL_DIR="$(pwd)/Docker/narwhal"
#
# ./buildApp -c --cappinstalldir="$CAPP_INSTALL_DIR"
# export PATH="$CAPP_INSTALL_DIR/bin:$PATH"

./buildApp -Ld --cappinstalldir="$CAPP_INSTALL_DIR" --setversion="1.0"

# cp -a ./Build/Deployment/SpecificationsDirector.ready ./Docker/app # we should use this, but it crashes.. I'll fix it later
cp -a ./Build/Deployment/SpecificationsDirector.pressed ./Docker/app

cd Docker
docker build -t monolithe/specsdirector-client .
cd -

rm -rf ./Docker/app
rm -rf ./Docker/cappuccino
rm -rf ./Docker/narwhal
