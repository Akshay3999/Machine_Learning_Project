from InsurancePremiumPrediction.config.configuration import Configuration
from InsurancePremiumPrediction.logger import logging
from InsurancePremiumPrediction.exception import InsuranceException

from InsurancePremiumPrediction.entity.artifact_entity import DataIngestionArtifact

from InsurancePremiumPrediction.entity.artifact_entity import DataValidationArtifact
from InsurancePremiumPrediction.component.data_ingestion import DataIngestion
from InsurancePremiumPrediction.component.data_validation import DataValidation
import sys
from collections import namedtuple
Experiment = namedtuple("Experiment", ["experiment_id", "initialization_timestamp", "artifact_time_stamp",
                                       "running_status", "start_time", "stop_time", "execution_time", "message",
                                       "experiment_file_path", "accuracy", "is_model_accepted"])


class Pipeline:
    experiment: Experiment = Experiment(*([None] * 11))
    experiment_file_path = None
    def __init__(self,config:Configuration=Configuration()) ->None:
        try:
            self.config=config

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())

            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                            data_ingestion_artifact=data_ingestion_artifact)

            return data_validation.initiate_data_validation()

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def start_data_transformation(self):
        pass

    def start_model_trainer(self):
        pass

    def start_model_evalution(self):
        pass

    def start_model_pusher(self):
        pass

    def run_pipeline(self):
        try:
            #data ingestion

            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise InsuranceException(e,sys) from e