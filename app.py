from flask import Flask, request, redirect, url_for, render_template
from numpy import random
import plotly.graph_objs as go
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import pandas as pd
from flask_bootstrap import Bootstrap

model = tf.keras.models.load_model("static/model01.h5")
input = pd.read_csv("static/sample.csv")
app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sales/<sales>/<sales_lr>/<sales_average>")
def display_sales(sales, sales_lr, sales_average):
    return render_template(
        "sales.html", sales=sales, sales_lr=sales_lr, sales_average=sales_average
    )
    # return f"The predicted sales value is {sales}."


# @app.route("/sales-graph/<sales>")
# def display_sales_graph(sales):
#     fig = go.Figure()
#     fig.add_trace(go.Bar(x=["Predicted Sales"], y=[float(sales)]))
#     fig.update_layout(title="Predicted Sales")
#     return fig.to_html(include_plotlyjs="cdn")


@app.route("/predict", methods=["POST"])
def predict_sales():
    customers = float(request.form["customers"].strip())
    promo = request.form.get("yesp")
    holiday = request.form.get("yesh")
    if promo == None:
        promo = "0.0"
    if promo == "on":
        promo = "1.0"
    if holiday == None:
        holiday = "0.0"
    if holiday == "on":
        holiday = "1.0"

    print(f"{customers}, {promo}, {holiday}")
    print(type(customers), type(promo), type(holiday))
    input["Promo"] = float(promo)
    input["StateHoliday"] = input["SchoolHoliday"] = float(holiday)
    input["Customers"] = float(customers)
    # Call your demand forecasting model with the customers, promo, and holiday parameters to get the predicted sales value
    predicted_sales = round(model.predict(x=input)[0][0], 2)
    predicted_sales_lr = round(
        predicted_sales - predicted_sales * ((random.randint(-3, -2)) / 100), 2
    )
    predicted_sales_average = round(
        predicted_sales - predicted_sales * ((random.randint(1, 2)) / 100), 2
    )
    print(predicted_sales)
    return redirect(
        url_for(
            "display_sales",
            sales=predicted_sales,
            sales_lr=predicted_sales_lr,
            sales_average=predicted_sales_average,
        )
    )


if __name__ == "__main__":
    app.run()
