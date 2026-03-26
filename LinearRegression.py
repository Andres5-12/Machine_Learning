import pandas as pd 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv("TSLA.csv")

df = df.dropna()

x = df[["Open"]]  
y = df[["Close"]] 

model = LinearRegression()
model.fit(x, y)

def predictPrice(open_price):
    result = model.predict([[open_price]])
    return float(result[0][0])