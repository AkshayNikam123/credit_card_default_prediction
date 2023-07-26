import os
import sys

from src.exception import CustomException
from src.util import load_object

class Predictor:
    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise CustomException(e, sys) from e
    
    @staticmethod
    def get_latest_model_path(model_dir):
        try:
            folder_name = list(map(int, os.listdir(model_dir)))
            latest_model_dir = os.path.join(model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise CustomException(e, sys) from e

    def predict(self, X):
        try:
            model_path = Predictor.get_latest_model_path(model_dir=self.model_dir)
            model = load_object(file_path=model_path)
            result = model.predict(X)
            return result
        except Exception as e:
            raise CustomException(e, sys) from e