#! /usr/bin/env python3

from abc import abstractmethod
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
ROOT = os.path.dirname(os.path.realpath(__file__))

TrainModelDB = namedtuple('TrainModelDB', ['key', 'status', 'out_file'])
ResponseRMQ = namedtuple('ResponseTrainRMQ', ['key', "data"])

class RMQHandlerBase:
    
    logger = logging.getLogger("MQTTHandler")

    def __init__(self, hostname, worker_port, queueName):
        self.host = hostname
        self.worker_port = worker_port
        self._thread = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.worker_port))
        self.channel = self.connection.channel()
    
        self.channel.queue_declare(queue=queueName, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queueName, on_message_callback=self.callback, auto_ack=True)
    
    def start(self, threadName):
        self._thread = threading.Thread(target=self.channel.start_consuming, name=threadName)
        self._thread.start()

    def callback(self, ch, method, properties, body):
        cmd = body.decode("utf-8")
        try:
            self.logger.debug("[x] Received %r" % cmd)
            cmd_dict = json.loads(cmd)
            resp = self._parse_request(cmd_dict)
        except json.decoder.JSONDecodeError as e:
            logging.error("Invalid JSON received from RMQ: %s" % cmd)
            return
        except TypeError as e:
            logging.error("Error occured while getting data from JSON, invalid type:\n", e)
            return
        except KeyError as e:
            logging.error("Error occured while parsing data from JSON, missed key:\n", e)
            return
        else:
            self.logger.debug("Request parsed successfully for key: %s" % resp.key)
            result = self._process_request(resp.key, resp.data)
            self._save_result(resp.key, result)
            logging.info(" [x] Done")

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
        key = request['key']
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
        key = request['key']    
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

def network_mock(model, dataset):
    return "mock result for model " + model + " and dataset " + dataset

def main():
    DBPort = os.environ.get("DB_PORT")
    trainWorkerPort = os.environ.get("TRAIN_QUEUE_PORT")
    predictorWorkerPort = os.environ.get("PREDICT_QUEUE_PORT")
    rmq_train = RMQHandlerTrain("worker_train_queue", trainWorkerPort, "train", db_handle.TrainModelDBMock(DBPort), network_mock)
    rmq_predict = RMQHandlerPredict("worker_predict_queue", predictorWorkerPort, "predict", db_handle.TrainModelDBMock(DBPort), network_mock)
    rmq_train.start()
    rmq_predict.start()
    logging.info(" [*] Waiting for messages. To exit press CTRL+C")
    while True:
        time.sleep(1)
    