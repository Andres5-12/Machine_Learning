import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score


df = pd.read_csv("mental_health.csv")
print(df.head())
print(df.info())
print(df.describe())
# Remove medium
df = df[df["burnout_level"] != "Medium"]

df = df.dropna()

# Encode
le = LabelEncoder()

df["burnout_level"] = le.fit_transform(df["burnout_level"])

X = df.drop("burnout_level",axis=1)

X = pd.get_dummies(X,drop_first=True)

y = df["burnout_level"]

X_train,X_test,y_train,y_test = train_test_split(

X,
y,
test_size=0.2,
random_state=42

)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000)

model.fit(X_train,y_train)

y_pred = model.predict(X_test)

y_prob = model.predict_proba(X_test)[:,1]


def getMetrics():

    accuracy = round(accuracy_score(y_test,y_pred),3)

    precision = round(precision_score(y_test,y_pred),3)

    recall = round(recall_score(y_test,y_pred),3)

    f1 = round(f1_score(y_test,y_pred),3)

    auc = round(roc_auc_score(y_test,y_prob),3)


    if not os.path.exists("static"):

        os.makedirs("static")


    # Confusion matrix

    cm = confusion_matrix(y_test,y_pred)

    plt.figure(figsize=(6,5))

    sns.heatmap(

        cm,
        annot=True,
        fmt='d',
        cmap="Blues"

    )

    plt.title("Confusion Matrix")

    plt.savefig("static/confusion_matrix.png")

    plt.close()


    # ROC

    fpr,tpr,_ = roc_curve(y_test,y_prob)

    plt.figure()

    plt.plot(fpr,tpr,label="AUC="+str(auc))

    plt.plot([0,1],[0,1],'--')

    plt.legend()

    plt.title("ROC Curve")

    plt.savefig("static/roc_curve.png")

    plt.close()


    return accuracy,precision,recall,f1,auc