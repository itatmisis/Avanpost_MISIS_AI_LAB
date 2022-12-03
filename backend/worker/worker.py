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
        self._threads = []
        connection_params = pika.ConnectionParameters(host=self.host, port=self.worker_port)
        pika.BlockingConnection = RMQHandlerBase.stable_connection(pika.BlockingConnection)
        self.connection = pika.BlockingConnection(connection_params)
        
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue=queueName, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queueName, on_message_callback=self.callback, auto_ack=False)
        # self.channel.start_consuming = RMQHandlerBase.stable_connection(self.channel.start_consuming)
    
    def start(self, threadName):
        self._thread = threading.Thread(target=self.channel.start_consuming, name=threadName)
        while True:
            try:
                self._thread.start()
            except Exception as e:
                self.logger.error("Error occured while starting thread: %s" % e)
                time.sleep(0.5)
            else:
                break
    
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

    def run_predictor_thread(self, resp, method):
        try:
            result = self._process_request(resp.key, resp.data)
            self._save_result(resp.key, result)
            self.logger.info(" [x] Done for key: %s" % resp.key)
        except Exception as e:
            self.logger.error("Error occured while processing request: %s" % e)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

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
            thread = threading.Thread(target=self.run_predictor_thread, args=(resp, method), name=str(resp.key), daemon=True)
            thread.start()
            self._threads.append(thread)

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
        dataset_path = "/datasets/" + str(request['dataset_path'])
        return ResponseRMQ(key, dataset_path) 

    def _process_request(self, key, dataset_path: str):
        model_path = "/models/" + str(key)
        self.logger.debug('Training model "%s" with dataset "%s"' % (model_path, dataset_path))
        self._data_handler.train(model_path, dataset_path)
        self.logger.debug('Model "%s" trained successfully' % model_path)
        result = "Done"
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
        image_path = "/images/" + str(request['image_path'])
        return ResponseRMQ(key, image_path)
    
    def _process_request(self, key, request):
        model_path = "/models/" + str(key)
        dataset_path = "/datasets/" + str(key)
        self.logger.debug('Predicting image "%s" with model "%s"' % (request, model_path))
        try:
            result = self._data_handler.predict(model_path, dataset_path, request)
        except FileNotFoundError as e:
            self.logger.warning(e)
            result = "Failed"
        else:
            self.logger.debug('Image predicted successfully, value is: %s' % str(result))
        return result

    def _save_result(self, key, result):
        self._database.save(key, result)

def main():
    logging.getLogger("MQTTHandler").setLevel(logging.DEBUG)
    logging.getLogger("ModelDBMock").setLevel(logging.DEBUG)
    logging.getLogger("pika").setLevel(logging.FATAL)
    DBPort = os.environ.get("DB_PORT")
    rabbitmqPort = os.environ.get("RABBITMQ_PORT")
    predictor = Predictor()
    rmq_train = RMQHandlerTrain("rabbitmq", rabbitmqPort, "train", db_handle.TrainModelDBMock(DBPort), predictor)
    rmq_predict = RMQHandlerPredict("rabbitmq", rabbitmqPort, "predict", db_handle.PredictModelDBMock(DBPort), predictor)
    rmq_train.start()
    rmq_predict.start()
    logger.info(" [*] Waiting for messages. To exit press CTRL+C")
    while True:
        time.sleep(1)
    
if __name__ == "__main__":
    main()