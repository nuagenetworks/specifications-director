#!/bin/bash

rm -rf specs
cp -a ../specs .
docker build -t monolithe/specsdirector-server .
rm -rf specs
