#!/bin/bash

cd app

echo -n "Which market (us/sg): "
read market

if [[ `echo $market | grep -v "us\|sg"` ]]; then
echo "Market $market is not configured, aborting.."
exit 1
fi

if [ ! -d data/$market ]; then
mkdir --parents data/$market
fi

python multi.py $market `cat stocks-$market`