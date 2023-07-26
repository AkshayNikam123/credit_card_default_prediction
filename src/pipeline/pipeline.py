from src.config.configuration import Configuration
from src.logger import logging
from src.exception import CustomException
from src.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact , DataTransformationArtifact
from src.entity.artifact_entity import ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_evaluation import ModelEvaluation
from src.components.model_trainer import ModelTrainer
from src.components.model_pusher import ModelPusher
import os ,sys
from threading import Thread
from collections import namedtuple


# We will inherit Thread class in Pipeline, to achieve parallel processing of training 
# to avoid page load delayin ui , we use thread, start pipeline and give response to user , training in progress
class Pipeline(Thread):
    RUNNING_STATUS = False
    def __init__(self, config:Configuration= Configuration())->None:
        try:
            super().__init__(daemon=False , name="pipeline")
            self.config=config
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
                raise CustomException(e, sys) from e

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact)-> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                             data_ingestion_artifact= data_ingestion_artifact, )
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise CustomException(e,sys) from e
            
    def start_data_transformation(self,
                                  data_ingestion_artifact:DataIngestionArtifact,
                                  data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        
        try:
            data_transformation =  DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact)
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise CustomException(e, sys) from e
    
    
    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                         data_transformation_artifact=data_transformation_artifact)
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise CustomException(e , sys) from e
            
    
    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               data_validation_artifact: DataValidationArtifact,
                               model_trainer_artifact: ModelTrainerArtifact,
                               )->ModelEvaluationArtifact:
        try:
            model_evaluation = ModelEvaluation(model_evaluation_config=self.config.get_model_evaluation_config(),
                                               data_ingestion_artifact=data_ingestion_artifact,
                                               data_validation_artifact=data_validation_artifact,
                                               model_trainer_artifact=model_trainer_artifact,
                                               )
            return model_evaluation.initiate_model_evaluation()
        except Exception as e:
            raise CustomException(e,sys) from e
    
    def start_model_pusher(self, model_evaluation_artifact:ModelEvaluationArtifact,
                           )->ModelPusherArtifact:
        try:
            model_pusher = ModelPusher(model_pusher_config=self.config.get_model_pusher_config(),
                                       model_evaluation_artifact=model_evaluation_artifact)
            
            return model_pusher.initiate_model_pusher()
        except Exception as e:
            raise CustomException(e, sys) from e
            
    
    def run_pipeline(self, ):
        try:
            RUNNING_STATUS = True
            # start data ingestion
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                    data_validation_artifact=data_validation_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact,
                                                                    )
            
            if model_evaluation_artifact.is_model_accepted:
                model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
                logging.info(f'Model pusher artifact: {model_pusher_artifact}')
            else:
                logging.info("Trained model rejected.")
            logging.info("Pipeline completed.")
            RUNNING_STATUS = False
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise CustomException(e, sys)