#!/bin/bash

cd app

echo -n "Which market (us/sg): "
read market

if [[ `echo $market | grep -v "us\|sg"` ]]; then
echo "Market $market is not configured, aborting.."
exit 1
fi

echo -n "Enter date (year-month-date): "
read datetime

python extractMissing.py $datetime $market `cat stocks-$market`