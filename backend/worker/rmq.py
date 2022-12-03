#! /usr/bin/env python3

from abc import abstractmethod
from functools import wraps
import functools
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

TrainModelDB = namedtuple('TrainModelDB', ['key', 'status', 'out_file'])
ResponseRMQ = namedtuple('ResponseTrainRMQ', ['key', "data"])
lock = threading.Lock()

class RMQHandlerBase:
    
    logger = logging.getLogger("MQTTHandler")

    def __init__(self, hostname, worker_port, login, password, queueName):
        self.host = hostname
        self.port = worker_port
        credentials = pika.PlainCredentials(login, password)
        self._thread = None
        self._threads = []
        connection_params = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        pika.BlockingConnection = RMQHandlerBase.stable_connection(pika.BlockingConnection)
        self.connection = pika.BlockingConnection(connection_params)
        
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queueName, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        on_message_callback = functools.partial(self.callback, args=[self.connection])
        self.channel.basic_consume(queue=queueName, on_message_callback=on_message_callback, auto_ack=False)

    
    def start(self, threadName):
        self._thread = threading.Thread(target=self.channel.start_consuming, name=threadName)
        self._thread.start()
        # while True:
        #     try:
                
        #     except Exception as e:
        #         self.logger.error("Error occured while starting thread: %s" % e)
        #         self._thread.join()
        #         time.sleep(0.5)
        #     else:
                # break
    
    @staticmethod
    def stable_connection(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            while True:
                try:
                    result = func(*args, **kwargs)
                except (pika.exceptions.AMQPConnectionError, pika.exceptions.StreamLostError) as e:
                    RMQHandlerBase.logger.warning("Connection error occured, trying to reconnect...")
                    time.sleep(0.5)
                except Exception as e:
                    RMQHandlerBase.logger.error("Error occured while running function: %s" % e)
                    time.sleep(0.5)
                else:
                    RMQHandlerBase.logger.info("Pika connection established")
                    break
            return result
        return wrapped

    def _ack_message(self, channel, delivery_tag):
        """Note that `channel` must be the same pika channel instance via which
        the message being ACKed was retrieved (AMQP protocol constraint).
        """
        if channel.is_open:
            channel.basic_ack(delivery_tag)
        else:
            # Channel is already closed, so we can't ACK this message;
            # log and/or do something that makes sense for your app in this case.
            pass

    def run_predictor_thread(self, connection, channel, delivery_tag, resp):
        try:
            result = self._process_request(resp.key, resp.data)
            self.logger.info(" [x] Done for key: %s" % resp.key)
        except Exception as e:
            self.logger.error("Error occured while processing request: %s" % e)
        # self.channel.basic_ack(delivery_tag=delivery_tag)
        cb = functools.partial(self._ack_message, channel, delivery_tag)
        connection.add_callback_threadsafe(cb)
                
    def callback(self, channel, method_frame, header_frame, body, args):
        def ack_message():
            cb = functools.partial(self._ack_message, channel, delivery_tag)
            connection.add_callback_threadsafe(cb)

        delivery_tag = method_frame.delivery_tag
        connection = args[0]
        try:
            cmd = body.decode("utf-8")
            self.logger.debug("[x] Received %r" % cmd)
            cmd_dict = json.loads(cmd)
            resp = self._parse_request(cmd_dict)
        except json.decoder.JSONDecodeError as e:
            self.logger.warning("Invalid JSON received from RMQ: %s" % cmd)
            ack_message()
        except TypeError as e:
            self.logger.warning("Error occured while getting data from JSON, invalid type.")
            ack_message()
        except KeyError as e:
            logging.warning("Error occured while parsing data from JSON, missed key.")
            ack_message()
        except Exception as e:
            self.logger.error("Error occured while parsing request.")
            ack_message()
        else:
            self.logger.debug("Request parsed successfully for key: %s" % resp.key)
            thread = threading.Thread(target=self.run_predictor_thread, args=(connection, channel, delivery_tag, resp), name=str(resp.key), daemon=True)
            thread.start()
            self._threads.append(thread)

    @abstractmethod
    def _parse_request(self, request: json):
        raise NotImplementedError
    
    @abstractmethod
    def _process_request(self, request):
        raise NotImplementedError


class RMQHandlerTrain(RMQHandlerBase):
    logger = logging.getLogger("MQTTHandler.Train")

    def __init__(self, hostname, worker_port, login, password, queueName, database, data_handler):
        self._data_handler = data_handler
        self._database = database
        super().__init__(hostname, worker_port, login, password, queueName)

    def start(self):
        return super().start("RMQHandlerTrain")

    def _parse_request(self, request: json):
        key = str(request['key'])
        dataset_path = "/datasets/default"
        # dataset_path = "/datasets/" + str(request['dataset_path'])
        return ResponseRMQ(key, dataset_path) 

    def _process_request(self, key, dataset_path: str):
        # model_path = "/models/" + str(key)
        model_path = "/models/model"
        self.logger.debug('Training model "%s" with dataset "%s"' % (model_path, dataset_path))
        self._data_handler.train(model_path, dataset_path)
        self.logger.debug('Model "%s" trained successfully' % model_path)
        result = "Done"
        # TODO: save update progress bar in db for key
        return result
    

class RMQHandlerPredict(RMQHandlerBase):

    logger = logging.getLogger("MQTTHandler.Predict")

    def __init__(self, hostname, worker_port, login, password, queueName, database, data_handler):
        self._data_handler = data_handler
        self._database = database
        super().__init__(hostname, worker_port, login, password, queueName)
    
    def start(self):
        return super().start("RMQHandlerPredict")

    def _parse_request(self, request: json):
        key = str(request['key'])
        image_path = "/images/" + str(request['image_filename'])
        return ResponseRMQ(key, image_path)
    
    def _process_request(self, key, request):
        # model_path = "/models/" + str(key)
        model_path = "/models/model"
        # dataset_path = "/datasets/" + str(key)
        dataset_path = "/datasets/default"
        self.logger.debug('Predicting image "%s" with model "%s"' % (request, model_path))
        self._database.in_progress(key)
        try:
            result = self._data_handler.predict(model_path, dataset_path, request)
        except FileNotFoundError as e:
            self.logger.warning("File not found: %s" % e)
            result = "Failed"
            self._database.error(key)
        else:
            self._database.update_progress(key, 100)
            self._database.update_class_name(key, result)
            self.logger.debug('Image predicted successfully, answer is: %s' % str(result))
        return result

