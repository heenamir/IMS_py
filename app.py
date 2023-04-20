from flask import Flask, request, redirect, url_for, render_template
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import pandas as pd

model = tf.keras.models.load_model('static/model01.h5')
input = pd.read_csv('static/sample.csv')
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sales/<sales>")
def display_sales(sales):
    return f"The predicted sales value is {sales}."

@app.route("/predict", methods=["POST"])
def predict_sales():
    customers = float(request.form["customers"].strip())
    promo = request.form.get("yesp")
    holiday = request.form.get("yesh")
    if(promo == None):
        promo = "0.0"
    if(promo == "on"):
        promo = "1.0"
    if(holiday == None):
        holiday = "0.0"
    if(holiday == "on"):
        holiday = "1.0"
    
    print(f'{customers}, {promo}, {holiday}')
    print(type(customers), type(promo), type(holiday))
    input['Promo'] = float(promo)
    input['StateHoliday'] = input['SchoolHoliday']  = float(holiday) 
    input['Customers'] = float(customers)
    # Call your demand forecasting model with the customers, promo, and holiday parameters to get the predicted sales value
    predicted_sales = model.predict(x=input)[0][0]
    print(predicted_sales)
    return redirect(url_for("display_sales", sales=predicted_sales))

if __name__ == "__main__":
    app.run()

