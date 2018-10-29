#!/bin/bash


# kill any previously running instances of this program
pkill -f '^python3[ ]kafka'

# get rid of the old log files 
[ -e "myprogram.out" ] && rm myprogram.out
[ -e "kafka_broker.log" ] && rm kafka_broker.log

# make sure anaconda got installed properly 
if ! python3 -V 2>/dev/null; then
    ln -s /root/anaconda/bin/python /usr/bin/python3
    ln -s /root/anaconda/bin/pip /usr/bin/pip3
fi

# install pip libraries 
pip3 -q install -r requirements.txt

# run it!
nohup python3 kafka_broker.py tweet > tweets.out 2>&1 &

nohup python3 kafka_broker.py survey > survey.out 2>&1 &