import logging

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
    