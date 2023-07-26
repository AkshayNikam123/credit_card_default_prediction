from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact , DataIngestionArtifact, DataValidationArtifact
import os,sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import  StandardScaler , OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.util import read_yaml_file , save_object , save_numpy_array_data , load_data
from src.constant import *
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator , TransformerMixin
import dill



class DataTransformation:
    def __init__(self , data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact):
        try:
            logging.info(f" {'='* 20} Data Transformation log started. {'='*20} ")
            
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys) from e
    
            

        
    def get_data_transformer_object(self)->Pipeline:
        try:
            schema_file_path  = self.data_validation_artifact.schema_file_path
            data_schema = read_yaml_file(file_path=schema_file_path)
            
            numerical_columns = data_schema[NUMERICAL_COLUMNS_KEY]
            
            
            preprocessing =  Pipeline(steps=[
                ('imputer' , SimpleImputer(strategy='median')),
                ('scaler',  StandardScaler())
                ])
            
            
            """
            We dont have categorical columns we are commenting this code
            categorical_columns = data_schema[CATEGORICAL_COLUMNS_KEY]
            cat_pipeline = Pipeline([
                ('impute' , SimpleImputer(strategy=['most_frequent'])),
                ('one_hot_encoder', OneHotEncoder()),
                ('scaler' , StandardScaler(with_mean=False)),
                ])
            
            preprocessing = ColumnTransformer([
                ('num_pipeline' , num_pipeline , numerical_columns),
                ('cat_pipeline' , cat_pipeline , categorical_columns)
            ])
            return preprocessing
            
            preprocessing = ColumnTransformer([
                ('num_pipeline' , num_pipeline , numerical_columns),
            ])
            """
            return preprocessing
        except Exception as e:
            raise CustomException(e, sys) from e
    

            
    def initiate_data_transformation(self, )-> DataTransformationArtifact:
        try:
            logging.info(f"Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()
            logging.info(f"Obtaining train,test file path")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            schema_file_path = self.data_validation_artifact.schema_file_path
            logging.info(f"Loading training and test data as pandas dataframe")
            train_df = load_data(file_path=train_file_path,schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)
            schema = read_yaml_file(schema_file_path)
            target_column = schema[TARGET_COLUMN_KEY]
            logging.info(f"Splitting input and target feature from train and test dataframe")
            input_feature_train_df = train_df.drop([target_column ,'ID'], axis=1)
            target_feature_train_df = train_df[target_column]
            # We will drop column 'ID' as its of not use for model 
           
            input_feature_test_df = test_df.drop([target_column,'ID'], axis=1)
            target_feature_test_df = test_df[target_column]
        
            logging.info(f"Applying preprocessing object on train and test dataframe and transforming data")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)
            
            
            train_arr = np.c_[input_feature_train_arr , np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr , np.array(target_feature_test_df)]
            
            transformed_train_dir = self.data_transformation_config.trasnformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir
            logging.info(f"Saving transformed train and test numpy array")
            
            train_file_name = os.path.basename(train_file_path).replace('.csv', '.npz')
            test_file_name = os.path.basename(test_file_path).replace('.csv', '.npz')
        
            transformed_train_file_path = os.path.join(transformed_train_dir , train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir , test_file_name)
            
            save_numpy_array_data(file_path=transformed_train_file_path , array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path , array=test_arr)
            
            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path
            logging.info(f"Saving preprocessing object")
            save_object(file_path=preprocessing_obj_file_path, obj= preprocessing_obj)
            
            data_transformation_artifact = DataTransformationArtifact(is_transformed="True",
                                                                      message="Data Transformation sucessful",
                                                                      transformed_train_file_path=transformed_train_file_path,
                                                                      transformed_test_file_path=transformed_test_file_path,
                                                                      preprocessed_object_file_path=preprocessing_obj_file_path)
            logging.info(f"Data transformation artifact : {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def __del__(self):
        logging.info(f"{'>>'*20} Data Transformation log completed.{'<<'*20} \n\n")