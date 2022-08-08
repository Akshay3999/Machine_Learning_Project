from setuptools import setup,find_packages
from typing import List


# Declaring variables for setup functions
PROJECT_NAME="InsurancePremiumPrediction"
VERSION="0.0.3"
AUTHOR="Akshay Tate"
DESCRIPTION="This is my first self made project"
REQUIREMENT_FILE_NAME="requirements.txt"

def get_requirements_list()->List[str]:

    """
    Description: This function is going to return list of requirement
    mention in requirementd.txt file
    
    return This function is going to return a list which contain name
    of libraries mentioned in requirements.txt file
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")

setup(
    name=PROJECT_NAME,
    version=VERSION,
    authOr=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirements_list()

)