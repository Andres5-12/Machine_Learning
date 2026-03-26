from flask import Flask, render_template, request
import LinearRegression

app = Flask (__name__)


@app.route('/FirstPage')
def homeJuan(): 
    return render_template ('Case1.html')

@app.route('/SecondPage')
def homeAndres(): 
    a=1
    return render_template ('Case2.html')

@app.route('/')
def firstPage(): 
    return render_template ('Page.html')

@app.route('/LinearRegression', methods=["GET","POST"])
def calculateGrade():
    calculateGrade = None
    if request.method == "POST":
        hours = float(request.form["hours"])
        calculateGrade = LinearRegression.calculateGrade(hours)
    return render_template("linearRegressionGrade.html", result=calculateGrade)