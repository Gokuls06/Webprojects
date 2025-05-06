from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import plotly.express as px
import plotly.io as pio
import io

app = Flask(__name__)

df = pd.DataFrame()
label_encoder = LabelEncoder()
model = LinearRegression()
locations = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global df, label_encoder, model, locations
    file = request.files['file']
    df = pd.read_csv(file)

    if not {'Rooms', 'SquareFoot', 'Location', 'Price'}.issubset(df.columns):
        return jsonify({'error': 'CSV must contain Rooms, SquareFoot, Location, and Price'}), 400

    df['Location_encoded'] = label_encoder.fit_transform(df['Location'])
    X = df[['Rooms', 'SquareFoot', 'Location_encoded']]
    y = df['Price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    locations = list(label_encoder.classes_)
    return jsonify({'message': 'Model trained successfully', 'locations': locations})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    rooms = int(data['rooms'])
    square_foot = int(data['square_foot'])
    location = data['location']

    location_encoded = label_encoder.transform([location])[0]
    input_data = [[rooms, square_foot, location_encoded]]
    predicted_price = model.predict(input_data)[0]

    lower_price = round(predicted_price * 0.9, -3)
    upper_price = round(predicted_price * 1.1, -3)

    return jsonify({'lower_usd': lower_price, 'upper_usd': upper_price})

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    usd_to_inr = 83.0
    lower_inr = round(data['lower_usd'] * usd_to_inr, -3)
    upper_inr = round(data['upper_usd'] * usd_to_inr, -3)
    return jsonify({'lower_inr': lower_inr, 'upper_inr': upper_inr})


if __name__ == '__main__':
    app.run(debug=True)
