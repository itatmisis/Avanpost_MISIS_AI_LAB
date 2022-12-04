"""
Python library to predict the class of an image using a trained model.
"""

__version__ = "0.0.1"
import predictor.inference as inference
import predictor.main as main

class Predictor:
    def predict(self, model_name, dataset_path, img_root):
        return inference.predict(model_name, dataset_path, img_root)

    def train(self, model_name, img_root, notyfier=None):
        return main.train_model(model_name, img_root, notyfier)