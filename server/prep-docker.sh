#!/bin/bash

CURRENT_PATH=`pwd`
rm -rf libs
mkdir libs

cd ../../bambou/
python setup.py sdist
cd $CURRENT_PATH
cp ../../bambou/dist/bambou*.tar.gz libs

cd ../../garuda/
python setup.py sdist
cd $CURRENT_PATH
cp ../../garuda/dist/garuda*.tar.gz libs

cd ../../monolithe/
python setup.py sdist
cd $CURRENT_PATH
cp ../../monolithe/dist/monolithe*.tar.gz libs

cd ..
../monolithe/commands/monogen-sdk -f specs -c specs/monoconf/config.ini
cd codegen
python setup.py sdist
cd $CURRENT_PATH
cp ../codegen/dist/specdk*.tar.gz libs