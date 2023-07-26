# Credit Card Default Prediction
### End To End Machine Learning Pipeline

## Project Demo Video Link : 
Youtube : https://youtu.be/vSqoueBL9WA

## Linkdn Profile : 
Linkdn : https://www.linkedin.com/in/nitinudmale/

## Product Description

The Credit Card Default Prediction project aims to develop a machine learning model that predicts whether a person will default on their credit card payment. The model utilizes historical payment data and various explanatory variables to make accurate predictions, helping financial institutions assess credit risk and make informed decisions.

## Background

Financial institutions encounter challenges in assessing creditworthiness and predicting default scenarios for credit card users. This project addresses these challenges by leveraging a binary variable, default payment (Yes = 1, No = 0), as the response variable. Additionally, the model uses 23 explanatory variables, including credit amount, gender, education level, marital status, age, history of past payment, bill statement amounts, and previous payment amounts. These variables provide crucial insights into an individual's credit behavior and financial stability.

## Explanatory Variables

The model uses the following 23 explanatory variables:

1. X1: Amount of the given credit (NT dollar): it includes both the individual consumer credit and his/her family (supplementary) credit.
2. X2: Gender (1 = male; 2 = female).
3. X3: Education (1 = graduate school; 2 = university; 3 = high school; 4 = others).
4. X4: Marital status (1 = married; 2 = single; 3 = others).
5. X5: Age (year).
6. X6 - X11: History of past payment. We tracked the past monthly payment records (from April to September, 2005) as follows: X6 = the repayment status in September, 2005; X7 = the repayment status in August, 2005; ...; X11 = the repayment status in April, 2005. The measurement scale for the repayment status is: -1 = pay duly; 1 = payment delay for one month; 2 = payment delay for two months; ...; 8 = payment delay for eight months; 9 = payment delay for nine months and above.
7. X12 - X17: Amount of bill statement (NT dollar). X12 = amount of bill statement in September, 2005; X13 = amount of bill statement in August, 2005; ...; X17 = amount of bill statement in April, 2005.
8. X18 - X23: Amount of previous payment (NT dollar). X18 = amount paid in September, 2005; X19 = amount paid in August, 2005; ...; X23 = amount paid in April, 2005.

## Methodology

The project follows a comprehensive approach that involves data preprocessing, feature selection, model training, and evaluation. It employs machine learning algorithms such as Logistic Regression, Random Forest, Gradient Boosting, Support Vector Machines (SVM), or Neural Networks for binary classification.

## Key Features

- Accurate Prediction: The model's accuracy ensures reliable credit risk assessment, reducing potential losses due to default scenarios.
- Explainable Predictions: The project incorporates interpretability techniques to explain the model's predictions and gain insights into contributing factors.
- Easy Integration: The trained model can be seamlessly integrated into existing systems for real-time credit evaluation.

## Pull Docker Container
* Access docker hub image of the project.
   ```bash
   docker pull nitin7478/creditcard_default_prediction

## Create Docker Container
Docker File Configuration :
![image](https://github.com/nitin7478/Credit-Card-Default-Prediction/assets/110007283/2010115b-9e2f-4a80-b53e-adea74efa04e)

1. Build docker image
   ```bash
   docker build -t username/project_name .
2. Run docker container 
   ```bash
   docker container run -d -p 7000:7000 username/project_name
3. List running container
   ```bash
   docker container ls
4. Stop container 
   ```bash
   docker container stop <first 3 or 4 digits of container>
Note : Run localhost:7000 on web browser after starting docker container.


## Installation Procedure
Installation Reference : https://packaging.python.org/en/latest/tutorials/packaging-projects/

1. Create a New Conda Environment:
   ```bash
   conda create -p venv python=3.10 -y
2. Activate the Conda Environment:
   ```bash
   conda activate venv/
3. upgrade pip:
   ```bash
   python -m pip install --upgrade pip
4. Install build package:
   ```bash
   python -m pip install --upgrade build
5. Install the Required Packages from pyproject.toml
   ```bash
   python -m build
6. This command will output a lot of text and once completed should generate two files in the dist directory:
   ```bash
   dist/
   ├── example_package_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
   └── example_package_YOUR_USERNAME_HERE-0.0.1.tar.gz
7. Install the Distribution File:
   ```bash
   python -m pip install dist/example_package_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
   



## Usage 
1. Main project folder         : /
2. Flask web page application  : /app.py
   ```bash
   python app.py
3. To train ml pipeline/model  : /pipeline.py
   ```bash
   python pipeline.py
   
Note : Run localhost:5000 on web browser to starting flask web app i.e. app.py

* Precautions(For Developers) : Precautions if user wants to train model pipeline in new system or in a new docker image, when already trained model is present in artifacts which is trained by another system, to avoid path conflicts, delete below mentioned folders.(For first time training only)
   ```bash
   Delete below mention folders to train model pipeline in new system.
   /src/artifact
   /Current_Model_Metric_Info
   /saved_models
   ```
   
## Configuration
Three main config files are present in /config folder.
1. config.yaml : It contains all the project related config details
2. model.yaml : It contains all model training related details. Change parameters in this file to perform hyperparameter tuning.
3. schema.yaml : It containes schema of the dataset for validation purpose.

## Dataset
The dataset used in this project can be found at [Dataset Link](https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip).

(Thanks For Dataset -> Credit : https://archive.ics.uci.edu )

## Project Structure
```bash

Credit-Card-Default-Prediction/
│
├── .dockerignore
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
├── Dockerfile
├── app.py
├── pipeline.py
├── requirements.txt
├── .ebextensions/
│   └── python.config
├── tests/
├── config/
│   ├── config.yaml
│   ├── model.yaml
│   └── schema.yaml
├── Current_Model_Metric_Info/
│   └── Current_Model_Metric_Info.csv
├── notebook/
│   └── ... (Jupyter notebooks)
├── saved_models/
│   └── ... (saved models)
├── templates/
│   └── ... (HTML templates for the web app)
├── Documents/
│   ├── High Level Design.pdf
│   ├── Low Level Design.pdf
│   └── Wireframe.pdf
└── src/
    ├── components/
    │   ├── __init__.py
    │   ├── data_ingestion.py
    │   ├── data_validation.py
    │   ├── data_transformation.py
    │   ├── model_trainer.py
    │   ├── model_evaluation.py
    │   └── model_pusher.py
    ├── config/
    │   ├── __init__.py
    │   └── configuration.py
    ├── constant/
    │   ├── __init__.py
    ├── entity/
    │   ├── __init__.py
    │   ├── artifact_entity.py
    │   ├── config_entity.py
    │   ├── model_factory.py
    │   └── predictor.py
    ├── pipeline/
    │   ├── __init__.py
    │   └── pipeline.py
    ├── __init__.py
    ├── exception.py
    ├── logger.py

```



## Project Structure
![image](https://github.com/nitin7478/Credit-Card-Default-Prediction/assets/110007283/ae03a7f4-89c9-4c78-b36b-dc86c3cb30af)







## Features

* On one click or command, program will start training pipeline, pipeline will perform below tasks in que.We can call these tasks as components of pipeline.
1. Data Ingestion : First current data,zip file , will be downloaded from given link and it will be extracted as raw data , then it will be splitted into training and test dataset. All the artifacts will be stored in data_ingestion folder.
2. Data Validation : Schema validation and data drift task will be performed in this component. We will be using evidently library to genrate data drift reports.All the artifacts will be stored in data_validation folder.
3. Data Transformation : Validated data will be transformed using preprocessing object as per project need.All the artifacts will be stored in data_transformation folder.
4. Model Trainer : Read the model.yaml file and perfomed model training using GridSearchCV, and store the best performing model object with preprocessing object, in single object,  in trained_model folder inside model_trainer artifact folder.
5. Model Evaluation : Evaulate the best performing model from previously , model_trainer artifact , with current model in production is any. If current trained model is better than previous model , replace previous with current model. We will keep best performing model. All the artifacts will be stored in Model_evaluation folder as model_evaluation.yaml. Then export the final model to src/saved_models folder for production.
* To experiment with model training parameters use , model.yaml file in src/config folder.


## License
[MIT](https://choosealicense.com/licenses/mit/)
