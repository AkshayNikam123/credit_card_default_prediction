from src.logger import logging 
from src.exception import CustomException
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
import sys,os
import tarfile , zipfile
import urllib.request
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit




class DataIngestion:
    def __init__(self , data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f" {'='* 20} Data Ingestion log started. {'='*20} ")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e , sys) from e
    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise CustomException(e , sys) from e
        
    def download_data(self, ) -> str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url
            
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)
                
            os.makedirs(tgz_download_dir , exist_ok = True)
            
            file_name = os.path.basename(download_url)
            
            tgz_file_path = os.path.join(tgz_download_dir , file_name)
            
            
            logging.info(f"Downloading file from : [{download_url}] into : [{tgz_file_path}]")
            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"File : [{tgz_file_path}] has been downloaded succesfully")
            
            return tgz_file_path
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def extract_tgz_file(self, tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir , exist_ok= True)
            logging.info(f"Extracting tgz/zip file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            
            if os.path.exists(tgz_file_path):
                with zipfile.ZipFile(tgz_file_path , 'r') as zip_file:
                    zip_file.extractall(raw_data_dir)
                    
            logging.info(f"Extraction completed")
            
        except Exception as e:
            raise CustomException(e , sys) from e
    
    def split_data_as_train_test(self,) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            
            file_name = os.listdir(raw_data_dir)[0]
            
            src_file_path = os.path.join(raw_data_dir, file_name)
            logging.info(f"Reading excel file: [{src_file_path}]")
            df = pd.read_excel(src_file_path , skiprows=1)
            # We are reading excel file and exporting csv as train and test file
            file_name = file_name.replace('.xls','.csv')
            logging.info(f"Splitting data into train and test")
            
            strat_train_set = None 
            strat_test_set = None
            stratified_shuffle_split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
            for train_index, test_index in stratified_shuffle_split.split(df, df['default payment next month']):
                strat_train_set = df.loc[train_index]
                strat_test_set = df.loc[test_index]
            
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir , exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path , index = False)
                
                
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir , exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path , index = False)
            
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                raw_file_path=src_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact
            
        except Exception as e:
            raise CustomException(e , sys) from e
        
    
    def __del__(self):
        logging.info(f"{'>>'*20} Data Ingestion log completed.{'<<'*20} \n\n")

# if __name__=="__main__":
#     a = DataIngestion()
#     a.download_data()
    
