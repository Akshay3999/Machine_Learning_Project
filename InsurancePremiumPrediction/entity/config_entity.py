from collections import namedtuple

TrainingPipelineConfig=namedtuple("TrainingPipelineConfig",["artifact_dir"])

DataIngestionConfig=namedtuple("DataIngestionConfig",
["dataset_dawnlod_url","tgz_dawnload_dir","raw_data_dir","ingested_train_dir","ingested_test_dir"])

DataVlidationConfig = namedtuple("DtaValidationConfig",["schema_file_path"])

DataTransformationConfig = namedtuple("DataTransformationConfig", ["transformed_train_dir",
                                                                   "transformed_test_dir",
                                                                   "preprocessed_object_file_path"])

ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["trained_model_file_path","base_accuracy"])

ModelEvaluationConfig = namedtuple("ModelEvaluationConfig", ["model_evaluation_file_path","time_stamp"])

ModelPusherConfig = namedtuple("ModelPusherConfig", ["export_dir_path"])