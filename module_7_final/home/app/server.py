import pandas as pd
import numpy as np
import pickle
from flask import Flask, request, jsonify
import preparation

with open('./models/model_opt.pkl', 'rb') as pkl_file: 
    model = pickle.load(pkl_file)

# создаём приложение
app = Flask(__name__)

@app.route('/')
def index():
    msg = "Тестовое сообщение. Сервер запущен!"
    return msg

@app.route('/predict', methods=['POST'])
def predict_func():    
    
    df = pd.read_json(request.json, dtype={str})    
    df = preparation.normalize_data(df)
    y_pred = np.exp(model.predict(df)) 
    
    return jsonify({'prediction': y_pred.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)