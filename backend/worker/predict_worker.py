#! /usr/bin/env python3

from abc import abstractmethod
from functools import wraps
import json
import os
import pika
import time
import logging
from collections import namedtuple
import requests as req
import threading
import db_handle
import sys
from predictor import Predictor
from rmq import RMQHandlerPredict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Worker.predict")

def main():
    logging.getLogger("MQTTHandler").setLevel(logging.DEBUG)
    logging.getLogger("ModelDBMock").setLevel(logging.DEBUG)
    logging.getLogger("PostgresDB.Predict").setLevel(logging.DEBUG)
    logging.getLogger("pika").setLevel(logging.FATAL)
    # DBPort = os.environ.get("DB_PORT")
    rabbitmqHost = os.environ.get("RMQ_HOST")
    rabbitmqPort = os.environ.get("RMQ_PORT")
    rabbitmqLogin = os.environ.get("RMQ_LOGIN")
    rabbitmqPassword = os.environ.get("RMQ_PASSWORD")
    predictor = Predictor()
    args = {
        "hostname": rabbitmqHost,
        "worker_port": rabbitmqPort,
        "login": rabbitmqLogin,
        "password": rabbitmqPassword,
        "queueName": "predict", 
        "database": db_handle.PredictModelDB(),
        "data_handler": predictor
    }
    rmq_predict = RMQHandlerPredict(**args)
    rmq_predict.start()
    logger.info(" [*] Waiting for messages. To exit press CTRL+C")
    while True:
        time.sleep(1)
    
if __name__ == "__main__":
    main()