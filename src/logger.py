import logging 
import os
from datetime import datetime
from src.constant import get_current_time_stamp


LOG_FILE = f"log_{get_current_time_stamp()}.log"
LOG_DIR = "logs"

logs_path = os.path.join(os.getcwd(),LOG_DIR)
os.makedirs(logs_path , exist_ok = True)
LOG_FILE_PATH = os.path.join(logs_path , LOG_FILE)
logging.basicConfig(
    filename = LOG_FILE_PATH,
    filemode="w",
    format = '[%(asctime)s] - %(levelname)s - %(lineno)d - %(filename)s - %(funcName)s() - %(message)s',
    level = logging.INFO,
)


# if __name__=="__main__":
#     logging.info("Logging has started")
    

# def get_latest_log_file_path():
#     try:
#         folder_name = list(map(int, os.listdir(model_dir)))
#         latest_model_dir = os.path.join(model_dir, f"{max(folder_name)}")
#         file_name = os.listdir(latest_model_dir)[0]
#         latest_model_path = os.path.join(latest_model_dir, file_name)
#         return latest_model_path
#     except Exception as e:
#         raise CustomException(e, sys) from e