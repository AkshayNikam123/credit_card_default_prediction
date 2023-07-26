from src.exception import CustomException
from src.logger import logging
import sys
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from src.util import load_numpy_array_data , save_object , load_object
from src.entity.model_factory import ModelFactory,MetricInfoArtifact,GridSearchedBestModel,evaluate_classification_model
from typing import List

# this class in not part of  pipeline , this is only for used in production
class EstimatorModel:
    def __init__(self , preprocessing_object , trained_model_object) -> None:
        """
        TrainedModel constructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
        
    def predict(self , X):
        """
        function accepts raw inputs and then trasnform the raw inputs using preprocessing_object ,
        which gaurantees that the inputs are in the same format as the training data
        At las it perfoem prediction on transformed data using trained_model_object
        """
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    
    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"
    
    

class ModelTrainer:
    def __init__(self , model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*30} Model trainer log started.{'<<'*30}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            
        except Exception as e:
            raise CustomException(e , sys) from e
    
    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            logging.info(f"Loading transformed training set")
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            train_array = load_numpy_array_data(transformed_train_file_path)
            
            logging.info(f"Loading transformed testing dataset")
            transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
            test_array = load_numpy_array_data(transformed_test_file_path)
        
            logging.info(f"Splitting transformed and testing input and target feature")
            x_train, y_train , x_test , y_test = train_array[:,:-1] , train_array[:,-1],test_array[:,:-1], test_array[:,-1]
            
            logging.info(f"Extracting model config file path")
            model_config_file_path = self.model_trainer_config.model_config_file_path
            
            logging.info(f"Initializing model factory class using above model config file : {model_config_file_path}")
            #Read model.yaml file from config folder, store in variable
            model_factory = ModelFactory(model_config_path = model_config_file_path)
            
            base_accuracy = self.model_trainer_config.base_accuracy
            logging.info(f"Expected accuracy : {base_accuracy}")
            
            logging.info(f"Initiating operation  model selection")
            #Get one best model and list of all models with results , only on train dataset
            best_model = model_factory.get_best_model(X = x_train , y=y_train , base_accuracy=base_accuracy)
            
            logging.info(f"Best model found on training dataset: {best_model}")
            
            logging.info(f"Extracting trained model list.")
            grid_searched_best_model_list:List[GridSearchedBestModel] = model_factory.grid_searched_best_model_list
            
            model_list = [model.best_model for model in grid_searched_best_model_list]
            logging.info(f"Evaluation all trained model on training and testing dataset both")
            
            metric_info:MetricInfoArtifact = evaluate_classification_model(model_list = model_list ,\
            X_train = x_train , y_train= y_train , X_test = x_test , y_test = y_test , base_accuracy=base_accuracy)
            
            
            logging.info(f"Best found model on both training and testing dataset.")     
                   
            #Load the object preprocessingObject
            preprocessing_obj=  load_object(file_path=self.data_transformation_artifact.preprocessed_object_file_path)
            model_object = metric_info.model_object

            #load trained model object
            trained_model_file_path=self.model_trainer_config.trained_model_file_path
            #We will use estimatormodel only in production for live prediction
            estimator_model = EstimatorModel(preprocessing_object=preprocessing_obj,trained_model_object=model_object)
            logging.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=estimator_model)


            model_trainer_artifact=  ModelTrainerArtifact(is_trained=True,message="Model Trained successfully",
            trained_model_file_path=trained_model_file_path,
            train_f1_score=metric_info.train_f1_score,
            test_f1_score=metric_info.test_f1_score,
            train_accuracy=metric_info.train_accuracy,
            test_accuracy=metric_info.test_accuracy,
            model_accuracy=metric_info.model_accuracy
            
            )

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
            
            
            
    def __del__(self):
        logging.info(f"{'=' * 20}Model Trainer log completed.{'=' * 20} ")
        
