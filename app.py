from flask import Flask
import sys
from InsurancePremiumPrediction.logger import logging
from InsurancePremiumPrediction.exception import InsuranceException
app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    try:
        raise Exception("We are testing custom exception")

    except Exception as e:
        Insurance = InsuranceException(e,sys)
        logging.info(Insurance.error_message)
        logging.info("We are testing logging module")
    return "CI CD pipline has been established and rerun"
    return "https://www.pexels.com/search/cat/"

if __name__=="__main__":
    app.run(debug=True)