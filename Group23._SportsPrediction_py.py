# -*- coding: utf-8 -*-
"""MidsemProject.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rRl17hjaUmAIkXazVpF3UjaDysnUoS_B
"""

from google.colab import drive
drive.mount('/content/drive')


"""Importing all the necessary libraries"""

import pandas as pd
import os
import sklearn
import numpy as np
import pandas as pd
import numpy as np, pandas as pd
from sklearn import tree, metrics
from sklearn.preprocessing import  LabelEncoder
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
from sklearn.model_selection import GridSearchCV, KFold
import streamlit as st
import pickle
import numpy as np

"""Reading the players 21 file and saving it in data"""

data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/players_21.csv')

data.info()

"""Picking out the columns with categorical values"""

categorical_columns = data.select_dtypes(include=['object', 'category']).columns

fifa = pd.DataFrame(data)

player_names = fifa['long_name']

"""## Encoding the categorical data using Label Encoder"""

selected_columns_df = fifa[categorical_columns]
label_encoder = LabelEncoder()

label_encoded = selected_columns_df.apply(lambda x: label_encoder.fit_transform(x))
categorical_values = pd.DataFrame(label_encoded)

fifa= fifa.drop(selected_columns_df ,axis=1)
fifa

"""Adding the encoded data samples back to the main dataset

"""

fifa = pd.concat([fifa,categorical_values], axis=1)
fifa.info()

"""## Feature Engineering"""

corr_matrix = fifa.corr()
low_corr_columns = corr_matrix.index[corr_matrix['overall'] < 0.6]
fifa = fifa.drop(columns=low_corr_columns)

"""Finding the samples with the maximum correlation and dropping the samples that fall beneath a certain threshold

"""

corr_matrix = fifa.corr()
corr_matrix["overall"].sort_values(ascending=False)
fifa
'overall', 'potential', 'realease_clause_eur',

"""## Imputing the missing values"""

fifa=fifa.fillna(method='ffill')
fifa=fifa.fillna(method='bfill')

"""Setting the"""

Y = fifa['overall']
X =fifa.drop("overall",axis=1)

X.head()

from sklearn.preprocessing import StandardScaler

"""## Scaling the data"""

x=StandardScaler()

scaled = x.fit_transform(X)
fifa = pd.DataFrame(scaled, columns=fifa.columns.drop('overall'))
X = fifa

X

Xtrain,Xtest,Ytrain,Ytest=train_test_split(X,Y,test_size=0.2,random_state=42)

"""## Training a model using XGBoost"""

xg = xgb.XGBRegressor(n_jobs=-1, eval_metric='mae')
xg.fit(Xtrain, Ytrain)
xg_pred = xg.predict(Xtest)

mse = mean_absolute_error(xg_pred,Ytest)
mse

"""# Training a model using Random Forest"""

rf=RandomForestRegressor()

rf= RandomForestRegressor(n_estimators=1000, random_state=42)

rf.fit(Xtrain, Ytrain)

rf_pred = rf.predict(Xtest)

"""## Using cross validation for the Random Forest Model"""

cv = KFold(n_splits=3)
PARAMETERS = {
    "max_depth": [2, 5, 6, 12],
    "n_estimators": [100, 500, 1000]
}
model_gs = GridSearchCV(rf, param_grid=PARAMETERS, cv=cv, scoring="neg_mean_absolute_error")
model_gs.fit(Xtrain, Ytrain)
y_pred = model_gs.best_estimator_.predict(Xtest)
y_pred

mae = mean_absolute_error(rf_pred,Ytest)

print("Mean absolute error :" ,mae)

"""## Training a model using Gradient Boosting"""

gbr = GradientBoostingRegressor()

gbr = GradientBoostingRegressor(n_estimators=100,learning_rate=0.05,random_state=50,max_features=5)

gbr.fit(Xtrain, Ytrain)

y_prediction = gbr.predict(Xtest)

y_prediction

mse_2 = mean_absolute_error(y_prediction,Ytest)

print("Mean absolute error :" ,mse_2)

"""## Loading and pre-processing the test data


"""

test_data = pd.read_csv('/content/drive/MyDrive/archive/players_22.csv')

categorical_columns = test_data.select_dtypes(include=['object', 'category']).columns
column_names = categorical_columns
column_names

fifa_test = pd.DataFrame(test_data)

"""## Imputing the missing values"""

fifa_test=fifa_test.fillna(method='ffill')
fifa_test=fifa_test.fillna(method='bfill')

Y_1 = fifa_test['overall']

"""## Encoding the data using Label encoding"""

selected_columns_df = fifa_test[column_names]
label_encoder = LabelEncoder()
label_encoded = selected_columns_df.apply(lambda x: label_encoder.fit_transform(x))
label_encoded
categorical_values = pd.DataFrame(label_encoded)

fifa_test= fifa_test.drop(selected_columns_df ,axis=1)
fifa_test

fifa_test = pd.concat([fifa_test,categorical_values], axis=1)
fifa_test.info()

"""## Creating a feature subset based on their correlation"""

corr_matrix = fifa_test.corr()
low_corr_columns = corr_matrix.index[corr_matrix['overall'] < 0.6]
fifa_test = fifa_test.drop(columns=low_corr_columns)
fifa_test.info()

X_1 =fifa_test.drop("overall",axis=1)

corr_matrix["overall"].sort_values(ascending=False)
fifa_test

"""#Scaling the data"""

sc=StandardScaler()

scaled1 = sc.fit_transform(X_1)
fifa_test = pd.DataFrame(scaled1, columns=fifa_test.columns.drop('overall'))
X_1 = fifa_test

X_1train,X_1test,Y_1train,Y_1test=train_test_split(X_1,Y_1,test_size=0.2,random_state=42)

"""## Using the gradient boost regressor model to predict the players overall rating"""

y1_prediction = gbr.predict(X_1test)

y1_prediction

mae_3 = mean_absolute_error(y1_prediction,Y_1test)

print("Mean absolute error :" ,mae_3)

"""## Using the XG Regressor model to predict the players overall rating"""

xg = xgb.XGBRegressor(learning_rate = 0.1,max_depth = 5,colsample_bytree = 0.5)
xg.fit(X_1train, Y_1train)

xg_predict = xg.predict( X_1test)
xg_predict

mse = mean_absolute_error(xg_pred,Ytest)
mse

"""## Using the random forest model to predict the players overall rating"""

y_pred = rf.predict(X_1test)

y_pred

mae = mean_absolute_error(y_pred, Y_1test)

mae

import pickle

pickle.dump(rf,open('rf.pkl','wb'))

with open('rf.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

st.title("Player Rating Predictor")

overall= st.number_input('overall', min_value=0.0, step=0.01, key='overall')
potential= st.number_input('potential', min_value=0.0, step=0.01, key='potential')
wage_eur = st.number_input('wage_eur', min_value=0.0, step=0.01, key='wage_eur')
passing = st.number_input('passing', min_value=0.0, step=0.01, key='passing')
dribbling = st.number_input('dribbling', min_value=0.0, step=0.01, key='dribbling')
movement_reactions = st.number_input('movement_reactions', min_value=0.0, step=0.01, key='movement_reactions')
mentality_composure = st.number_input('mentality_composure', min_value=0.0, step=0.01, key='mentality_composure')
lf = st.number_input('lf', min_value=0.0, step=0.01, key='lf')
cf = st.number_input('cf', min_value=0.0, step=0.01, key='cf')
rf = st.number_input('rf', min_value=0.0, step=0.01, key='rf')
lam = st.number_input('lam', min_value=0.0, step=0.01, key='lam')
cam = st.number_input('cam', min_value=0.0, step=0.01, key='cam')
ram = st.number_input('ram', min_value=0.0, step=0.01, key='ram')
lm = st.number_input('lm', min_value=0.0, step=0.01, key='lm')
lcm = st.number_input('lcm', min_value=0.0, step=0.01, key='lcm')
cm = st.number_input('cm', min_value=0.0, step=0.01, key='cm')
rcm = st.number_input('rcm', min_value=0.0, step=0.01, key='rcm')
rm = st.number_input('rm', min_value=0.0, step=0.01, key='rm')

if st.button("Predict"):
    input_data = np.array([[overall, potential, wage_eur, passing, dribbling, movement_reactions, mentality_composure, lf, cf, rf, lam, cam, ram, lm, lcm, cm, rcm, rm]])

    prediction = model.predict(input_data)[0]
    confidence_score = model.predict_proba(input_data).max() * 100

    st.write(f"Player Rating Prediction: {prediction:.2f}")
    st.write(f"Confidence Score: {confidence_score:.2f}%")
user_feedback = st.radio("Do you agree with the prediction?", ["Yes", "No"])
if user_feedback == "Yes":
    st.write("Thank you for your feedback!")
else:
    st.write("We appreciate your input. Please provide more details for better accuracy.")
