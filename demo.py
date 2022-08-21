from InsurancePremiumPrediction.pipeline.pipeline import Pipeline
from InsurancePremiumPrediction.exception import InsuranceException
from InsurancePremiumPrediction.logger import logging
from InsurancePremiumPrediction.config.configuration import Configuration

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
        # data_validation_config = Configuration().get_data_validation_config()
        # print(data_validation_config)
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=="__main__":
    main()