import logging
import psycopg2 
from peewee import *
import os
import logging
logger = logging.getLogger("PostgresDB")



credintials = {
    "host": os.environ.get("POSTGRES_HOST"),
    "port": os.environ.get("POSTGRES_PORT"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "database": os.environ.get("POSTGRES_DB")
}
db = PostgresqlDatabase(**credintials)
db.connect()

class predict(Model):
    id = IntegerField(primary_key=True)
    key = TextField()
    status = IntegerField()
    percent = DoubleField()
    class_name = TextField()
    class Meta:
        database = db
        database_table = 'predict'

class PredictModelDB:
    DONE = 2
    PENDING = 0
    IN_PROGRESS = 1
    ERROR = 3
    _logger = logging.getLogger("PostgresDB.Predict")

    def pending(self, key):
        self.update_status(key, self.PENDING)
    
    def in_progress(self, key):
        self.update_status(key, self.IN_PROGRESS)

    def done(self, key):
        self.update_status(key, self.DONE)

    def error(self, key):
        self.update_status(key, self.ERROR)
    
    def validate_key(self, key):
        try:
            return predict.get(predict.key == key)
        except Exception:
            self._logger.error("Error while validating key in DB: {}".format(key))
            return False

    def update_status(self, key, status):
        self.validate_key(key)
        try:
            predict.update(status=status).where(predict.key == key).execute()
        except Exception as e:
            self._logger.error("Error while updating status in DB: {}".format(e))

    def update_class_name(self, key, class_name):
        self.validate_key(key)
        try:
            predict.update(class_name=class_name).where(predict.key == key).execute()
        except Exception as e:
            self._logger.error("Error while updating class_name in DB: {}".format(e))
    
    def update_progress(self, key, percent):
        self.validate_key(key)
        try:
            predict.update(percent=percent).where(predict.key == key).execute()
        except Exception as e:
            self._logger.error("Error while updating progress in DB: {}".format(e))
    


class TrainModelDBMock:
    logger = logging.getLogger("ModelDBMock.Train")
    def __init__(self, dbPort):
        self.dbPort = dbPort

    def save(self, key, result):
        self.logger.info("Saving result for key %s to db: %s" % (key, result))
    
    def update_status(self, key, status):
        self.logger.info("Updating status for key %s to db: %s" % (key, status))
    
class PredictModelDBMock:
    logger = logging.getLogger("ModelDBMock.Predict")
    def __init__(self, dbPort):
        self.dbPort = dbPort

    def save(self, key, result):
        self.logger.info("Saving result for key %s to db: %s" % (key, result))
    

# Очередь train: {"key":"default", "dataset_path":"default"}
# Очередь predict: {"key":"abc", "image_filename":"default.jpg"}