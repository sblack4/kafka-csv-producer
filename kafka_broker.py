#!/usr/bin/env python

# standard libraries
from __future__ import print_function
import config
import json
from csv import DictReader
from datetime import datetime
import logging
from random import randrange
from time import sleep

# kafka-python libraries
from kafka import KafkaProducer
from kafka.errors import KafkaError


def run_kafka_broker(streamChoice):
    """sends a new datum every x seconds to kafka
    
    """
    if "tweet" in streamChoice:
        log_file = config.log_file 
        topic = config.topic
        key = config.key
        csv_file = config.csv_file
    else: 
        log_file = config.log_file1
        topic = config.topic1
        key = config.key1
        csv_file = config.csv_file1


    logging.basicConfig(filename=log_file,level=config.log_level)
    logging.info("logging to " + config.kafka_host)
    mykafkaservers = [config.kafka_host]
    producer = KafkaProducer(
        bootstrap_servers=mykafkaservers, 
        value_serializer=lambda m: m.encode('utf-8'),
        key_serializer=str.encode,
        api_version=(0,10,1)
    )

    produce = lambda vals: producer.send(topic, value=vals, key=key+str(datetime.now()).replace(' ', ':'))
    while True:
        fh = DictReader(open(csv_file))
        for row in fh:
            line = json.dumps(row)
            logging.info("line# " + "\n line: " + line)
            produce(line)
            sleep(config.timeout)


if __name__ == "__main__":
    from sys import argv
    run_kafka_broker(argv[1])
