from flask import Flask, render_template

app = Flask (__name__)


@app.route('/Juan')
def homeJuan(): 
    return render_template ('Garcia.html')

@app.route('/Andres')
def homeAndres(): 
    return render_template ('Corredor.html')

@app.route('/')
def firstPage(): 
    return render_template ('Page.html')