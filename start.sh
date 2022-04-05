#!/bin/bash

cd app

if [ ! -d data ]; then
mkdir data
fi

python multi.py `cat stocks`