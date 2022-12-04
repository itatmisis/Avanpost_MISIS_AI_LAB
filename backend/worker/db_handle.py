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

class train(Model):
    id = IntegerField(primary_key=True)
    key = TextField()
    status = IntegerField()
    percent = DoubleField()
    dataset = TextField()
    class Meta:
        database = db
        database_table = 'train'

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
            predict.get(predict.key == key)
        except Exception:
            self._logger.error("Error while validating key in DB: {}".format(key))
            return False
        return True

    def update_status(self, key, status):
        if not self.validate_key(key):
            return
        try:
            predict.update(status=status).where(predict.key == key).execute()
        except Exception as e:
            self._logger.error("Error while updating status in DB: {}".format(e))

    def update_class_name(self, key, class_name):
        if not self.validate_key(key):
            return
        try:
            predict.update(class_name=class_name).where(predict.key == key).execute()
        except Exception as e:
            self._logger.error("Error while updating class_name in DB: {}".format(e))
    
    def update_progress(self, key, percent):
        if not self.validate_key(key):
            return
        try:
            predict.update(percent=percent).where(predict.key == key).execute()
        except Exception as e:
            self._logger.error("Error while updating progress in DB: {}".format(e))
    
class TrainModeDB:
    DONE = 2
    PENDING = 0
    IN_PROGRESS = 1
    ERROR = 3
    _logger = logging.getLogger("PostgresDB.Train")

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
            train.get(train.key == key)
        except Exception as e:
            self._logger.error("Error while validating key \"{}\" in DB: {}".format(key, e))
            return False
        return True

    def update_status(self, key, status):
        if not self.validate_key(key):
            return
        try:
            train.update(status=status).where(train.key == key).execute()
        except Exception as e:
            self._logger.error("Error while updating status in DB: {}".format(e))

    def update_progress(self, key, percent):
        if not self.validate_key(key):
            return
        try:
            train.update(percent=percent).where(train.key == key).execute()
        except Exception as e:
            self._logger.error("Error while updating progress in DB: {}".format(e))
    
    def update_dataset_name(self, key, dataset):
        if not self.validate_key(key):
            return
        try:
            train.update(dataset=dataset).where(train.key == key).execute()
        except Exception as e:
            self._logger.error("Error while updating dataset name in DB: {}".format(e))

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

if __name__ == "__main__":
    from time import sleep
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("PostgresDB").setLevel(logging.DEBUG)
    train_db = TrainModeDB()
    predict_db = PredictModelDB()
    train.delete().where(train.key == "test").execute()
    predict.delete().where(predict.key == "test").execute()
    train.delete().where(train.key == "test_db_train").execute()
    predict.delete().where(predict.key == "test_db_predict").execute()
    predict.insert(key="test_db_predict", status=0, percent=0, class_name="").execute()
    train.insert(key="test_db_train", status=0, percent=0, dataset="").execute()
    train_db.pending("test_db_train")
    sleep(1)
    train_db.in_progress("test_db_train")
    sleep(1)
    train_db.done("test_db_train")
    sleep(1)
    train_db.error("test_db_train")
    sleep(1)
    predict_db.pending("test_db_predict")
    sleep(1)
    predict_db.in_progress("test_db_predict")
    sleep(1)
    predict_db.done("test_db_predict")
    sleep(1)
    predict_db.error("test_db_predict")
    sleep(1)
    train.delete().where(train.key == "test_db_train").execute()
    predict.delete().where(predict.key == "test_db_predict").execute()
