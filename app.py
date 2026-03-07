from flask import Flask, render_template

app = Flask (__name__)


@app.route('/')
def home(): 
    return render_template ('Garcia.html')


@app.route('/FirstPage/<name>')
def firstPage(name): 
    return render_template ('Garcia.html',name=name)