from flask import Flask, render_template, request
from src.entity.predictor import Predictor
import os,sys
import pandas as pd
from datetime import datetime
import csv 
from src.util.util import get_log_content
import subprocess

SAVED_MODELS_DIR_NAME = "saved_models"
ROOT_DIR = os.getcwd()
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


app = Flask(__name__)


def get_current_model_details(model_dir):
    """
    This function will return accuracy and training date of current model in production
    args : model_dir:str
    params: current_accuracy:float
    """
    last_trained_model_date = None
    current_accuracy = None
    line = list()
    METRIC_INFO_FILE_PATH = os.path.join(ROOT_DIR, 'Current_Model_Metric_Info', 'Current_Model_Metric_Info.csv' )
    if os.path.exists(METRIC_INFO_FILE_PATH):
        with open(METRIC_INFO_FILE_PATH, mode ='r') as file:
            csv_file = csv.reader(file)
            for lines in csv_file:
                line.append(lines)
        current_accuracy = round(float(line[0][-2]),2) *100
    else:
        current_accuracy = None
    if os.path.exists(model_dir):
        latest_model_folder_name = Predictor.get_latest_model_path(model_dir=model_dir)
        date_string = os.path.basename(os.path.dirname(latest_model_folder_name))
        last_trained_model_date = datetime.strptime(date_string, "%Y%m%d%H%M%S")
    else:
        last_trained_model_date = None
    return last_trained_model_date , current_accuracy

@app.route('/')
def home():
    last_trained_model_date , current_accuracy =  get_current_model_details(model_dir=MODEL_DIR)
    return render_template('index.html' ,last_trained_model_date=last_trained_model_date , current_accuracy=current_accuracy)



@app.route('/predict', methods=['POST'])
def predict():
    features = ['LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE', 'PAY_0',
                'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1',
                'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
                'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']

    input_data = pd.DataFrame(columns=features)
    input_row = {}
    for feature in features:
        input_value = request.form.get(feature)
        try:
            input_value = int(input_value)
        except ValueError:
            input_value = 0
        input_row[feature] = [input_value]
    input_data = pd.DataFrame.from_dict(input_row)
    # Perform prediction using the loaded model
    if os.path.exists(MODEL_DIR):
        predictor = Predictor(model_dir=MODEL_DIR)
        prediction = predictor.predict(input_data)
    else:
        prediction = None
    
    if prediction is not None:
        if prediction == 0:
            result = 'Not Default'
        else:
            result = 'Default'
    else:
        result = None
    return render_template('index.html', prediction_result=result )


@app.route('/trainer')
def trainer():
    return render_template('trainer.html')

@app.route('/start_trainer')
def start_trainer():
    subprocess.run(["python", "pipeline.py"])
    log_content = get_log_content()
    return render_template('start_trainer.html', logs=log_content)



if __name__ == '__main__':
    app.run()
    
    
    

