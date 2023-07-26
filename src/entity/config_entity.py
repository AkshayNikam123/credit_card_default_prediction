from collections import namedtuple

# we are defining structure of entity 

DataIngestionConfig =  namedtuple("DataIngestionConfig" , 
["dataset_download_url" , "tgz_download_dir","raw_data_dir","ingested_train_dir","ingested_test_dir"])

DataValidationConfig = namedtuple("DataValidationConfig", ["schema_file_path","report_file_path",
                                                           "report_page_file_path","data_drift_check_old_period"])

DataTransformationConfig = namedtuple("DataTransformationConfig", ["trasnformed_train_dir",
                                                                    "transformed_test_dir",
                                                                    "preprocessed_object_file_path"] )

ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["trained_model_file_path" , "base_accuracy",
                                                       "model_config_file_path"])

#  model_evaluation_file_path = model in production
ModelEvaluationConfig = namedtuple("ModelEvaluationConfig", ["Model_evaluation_file_path", "time_stamp"])

ModelPusherConfig = namedtuple("ModelPusherConfig", ["export_dir_path"])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"] )


