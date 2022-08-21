from InsurancePremiumPrediction.constant import *
from InsurancePremiumPrediction.entity.config_entity import DataValidationConfig
from InsurancePremiumPrediction.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from InsurancePremiumPrediction.logger import logging
from InsurancePremiumPrediction.exception import InsuranceException
from InsurancePremiumPrediction.util.util import read_yaml_file
import os,sys
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection   
import json
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab


class DataValidation:
    
    def __init__(self,data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'#'*20} Data Validation Log Started .{'#'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_train_and_test_df(self,):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_def = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_def
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def in_train_test_file_exits(self)->bool:
        try:
            logging.info(f"{'#'*20} Checking is Train and Test File is available or not . {'#'*20}")
            is_train_file_exist=False
            is_test_file_exist=False
            
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            is_train_file_exist=os.path.exists(train_file_path)
            is_test_file_exist=os.path.exists(test_file_path)

            is_available=is_train_file_exist and is_test_file_exist
            
            if not is_available:
                message=f"Training File Path { train_file_path } or Testing File Path { test_file_path } \
                is not available."
                logging.error(message)
        except Exception as e:
            raise InsuranceException from e

    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False
            schema_file_path=self.data_validation_config.schema_file_path
            schema_data=read_yaml_file(file_path=schema_file_path)
            schema_columns=schema_data['columns']
            schema_datatype_dataframe=pd.DataFrame.from_dict(schema_columns,orient='index')
            
            train_file_path=self.data_ingestion_artifact.train_file_path
            train_df=pd.read_csv(train_file_path)
            
            train_datatype_dataframe=pd.DataFrame(train_df.dtypes)
            if schema_datatype_dataframe.equals(train_datatype_dataframe):
                validation_status=True
                logging.info("Data columns and datatype validation completed")
            else:
                logging.info("Data validation faliure : data type not same or columns name mismatch")
            return validation_status
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_def,test_def = self.get_train_and_test_df()

            profile.calculate(train_def,test_def)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(self.data_validation_config.report_file_path,"w") as report_file:
                json.dump(report,report_file, indent=6)

            return report

        
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_def,test_def = self.get_train_and_test_df()
            dashboard.calculate(train_def,test_def)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir= os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(self.report_page_file_path)
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()      
            return True
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_test_file_exists()
            is_validated=self.validate_dataset()
            if is_validated:
                message=f"{'*'*20} Data Validate Successfully"
            else:
                message=f"{'*'*20} Data Validation Unsuccessful"
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=is_validated,
                message=message)

            return data_validation_artifact
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>'*20} Data Valdiation Log Completed{'<'*20}")