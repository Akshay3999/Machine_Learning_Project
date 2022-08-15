from curses import raw
import logging
import sys
from tkinter import E
from InsurancePremiumPrediction.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataVlidationConfig, \
    ModelEvaluationConfig, ModelTrainerConfig, ModelPusherConfig,TrainingPipelineConfig
from InsurancePremiumPrediction.util.util import read_yaml_file
from InsurancePremiumPrediction.logger import logger
import sys,os
from InsurancePremiumPrediction.constant import *
from InsurancePremiumPrediction.exception import InsuranceException



class Configuration:

    def __init__(self,
    config_file_path:str=CONFIG_FILE_NAME,
    current_time_stamp:str=CURRENT_TIME_STAMP
    )->None:
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.get_training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            artifact_dir = self.get_training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )
            data_ingestion_info=self.config_info.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_dawnload_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            tgz_dawnload_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]

            )

            raw_data_dir=os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])

            ingested_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )

            ingested_train_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )

            ingested_test_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )

            data_ingestion_config = DataIngestionConfig(
            dataset_dawnload_url=dataset_dawnload_url,
            tgz_dawnload_dir=tgz_dawnload_dir,
            data_ingestion_config=data_ingestion_config,
            ingested_test_dir=ingested_test_dir
            )
            
            logging.info(f"Data Ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise InsuranceException(e,sys) from e


    def get_data_validation_config(self)-> DataVlidationConfig:
        pass

    def data_transformation_config(self)-> DataTransformationConfig:
        pass

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        pass

    def get_model_evalution_config(self)->ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self) ->ModelPusherConfig:
        pass

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            trainin_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipeline config: {trainin_pipeline_config}")
            return trainin_pipeline_config
        except Exception as e:
            raise InsuranceException(e,sys) from e