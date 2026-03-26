from flask import Flask, render_template, request
from LinearRegression import predictPrice

app = Flask (__name__)


@app.route('/FirstPage')
def firstpage(): 
    return render_template ('Case1.html')

@app.route('/SecondPage')
def secondpage(): 
    return render_template ('Case2.html')

@app.route('/ThirdPage')
def  thirdpage(): 
    return render_template ('Case3.html')

@app.route('/FourthPage')
def fourthpage(): 
    return render_template ('Case4.html')

@app.route('/')
def homePage(): 
    return render_template ('Page.html')

@app.route('/LinearRegression', methods=["GET","POST"])
def predictPriceRoute():
    result = None

    if request.method == "POST":
        open_price = float(request.form["open_price"])
        result = predictPrice(open_price)

    return render_template("linearRegressionPrice.html", result=result)