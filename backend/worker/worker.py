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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Worker")
ROOT = os.path.dirname(os.path.realpath(__file__))

TrainModelDB = namedtuple('TrainModelDB', ['key', 'status', 'out_file'])
ResponseRMQ = namedtuple('ResponseTrainRMQ', ['key', "data"])

class RMQHandlerBase:
    
    logger = logging.getLogger("MQTTHandler")

    def __init__(self, hostname, worker_port, queueName):
        self.host = hostname
        self.worker_port = worker_port
        self._thread = None
        connection_params = pika.ConnectionParameters(host=self.host, port=self.worker_port)
        pika.BlockingConnection = RMQHandlerBase.stable_connection(pika.BlockingConnection)
        self.connection = pika.BlockingConnection(connection_params)
        
        self.channel = self.connection.channel()
    
        self.channel.queue_declare(queue=queueName, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queueName, on_message_callback=self.callback, auto_ack=True)
        # self.channel.start_consuming = RMQHandlerBase.stable_connection(self.channel.start_consuming)
    
    def start(self, threadName):
        self._thread = threading.Thread(target=self.channel.start_consuming, name=threadName)
        self._thread.start()
    
    @staticmethod
    def stable_connection(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            while True:
                try:
                    result = func(*args, **kwargs)
                except (pika.exceptions.AMQPConnectionError) as e:
                    RMQHandlerBase.logger.warning("Connection error occured, trying to reconnect...")
                    time.sleep(0.5)
                else:
                    RMQHandlerBase.logger.info("Pika connection established")
                    break
            return result
        return wrapped



    def callback(self, ch, method, properties, body):
        cmd = body.decode("utf-8")
        try:
            self.logger.debug("[x] Received %r" % cmd)
            cmd_dict = json.loads(cmd)
            resp = self._parse_request(cmd_dict)
        except json.decoder.JSONDecodeError as e:
            self.logger.warning("Invalid JSON received from RMQ: %s" % cmd)
            return
        except TypeError as e:
            self.logger.warning("Error occured while getting data from JSON, invalid type:\n", e)
            return
        except KeyError as e:
            logging.warning("Error occured while parsing data from JSON, missed key:\n", e)
            return
        else:
            self.logger.debug("Request parsed successfully for key: %s" % resp.key)
            result = self._process_request(resp.key, resp.data)
            self._save_result(resp.key, result)
            self.logger.info(" [x] Done for key: %s" % resp.key)

    @abstractmethod
    def _parse_request(self, request: json):
        raise NotImplementedError
    
    @abstractmethod
    def _process_request(self, request):
        raise NotImplementedError

    @abstractmethod
    def _save_result(self, key, result):
        raise NotImplementedError

class RMQHandlerTrain(RMQHandlerBase):
    logger = logging.getLogger("MQTTHandler.Train")

    def __init__(self, hostname, worker_port, queueName, database, data_handler):
        self._data_handler = data_handler
        self._database = database
        super().__init__(hostname, worker_port, queueName)

    def start(self):
        return super().start("RMQHandlerTrain")

    def _parse_request(self, request: json):
        key = str(request['key'])
        dataset_path = "/datasets/" + key
        return ResponseRMQ(key, dataset_path) 

    def _process_request(self, key, dataset_path: str):
        result = self._data_handler.train(dataset_path)
        # TODO: save update progress bar in db for key
        return result
    
    def _save_result(self, key, result):
        self._database.save(key, result)

class RMQHandlerPredict(RMQHandlerBase):

    logger = logging.getLogger("MQTTHandler.Predict")

    def __init__(self, hostname, worker_port, queueName, database, data_handler):
        self._data_handler = data_handler
        self._database = database
        super().__init__(hostname, worker_port, queueName)
    
    def start(self):
        return super().start("RMQHandlerPredict")

    def _parse_request(self, request: json):
        key = str(request['key'])
        image_path = "/images/" + key
        return ResponseRMQ(key, image_path)
    
    def _process_request(self, key, request):
        model = self._load_model(key)
        result = self._data_handler.predict(model, request)
        return result

    def _load_model(self, key):
        return "mock model for key " + key

    def _save_result(self, key, result):
        self._database.save(key, result)

class NetworkMock:
    @staticmethod
    def train(dataset):
        "mock result for training dataset " + dataset
    
    @staticmethod
    def predict(model, image_path):
        "mock result for model " + model + " and image " + image_path

def main():
    logging.getLogger("MQTTHandler").setLevel(logging.DEBUG)
    logging.getLogger("ModelDBMock").setLevel(logging.DEBUG)
    logging.getLogger("pika").setLevel(logging.FATAL)
    DBPort = os.environ.get("DB_PORT")
    rabbitmqPort = os.environ.get("RABBITMQ_PORT")
    rmq_train = RMQHandlerTrain("rabbitmq", rabbitmqPort, "train", db_handle.TrainModelDBMock(DBPort), NetworkMock)
    rmq_predict = RMQHandlerPredict("rabbitmq", rabbitmqPort, "predict", db_handle.PredictModelDBMock(DBPort), NetworkMock)
    rmq_train.start()
    rmq_predict.start()
    logger.info(" [*] Waiting for messages. To exit press CTRL+C")
    while True:
        time.sleep(1)
    
if __name__ == "__main__":
    main()