from src.pipeline.pipeline import Pipeline
from src.exception import CustomException
from src.logger import logging
from src.config.configuration import Configuration
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
from src.components.data_validation import DataValidation
import os

def main(): 
    try:        
        pipeline = Pipeline()
        pipeline.start()
        logging.info("main function execution completed")
        pipeline.join()
        # a = Configuration().get_data_transformation_config()
        # print(a)
    except Exception as e:
        logging.error(f"{e}")
        print(e)
    
if __name__=="__main__":
    main()
    

