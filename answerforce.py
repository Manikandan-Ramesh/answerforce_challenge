# -*- coding: utf-8 -*-
"""AnswerForce.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pDDIl51Vxi_KETYrPcQsZ_xz1iuvf3K7
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

att = pd.read_excel('account_attributes.xlsx')
acc = pd.read_excel('account_usage.xlsx')

att.head(5)

acc.head(5)

att.isnull().sum()

acc.isnull().sum()

acc.describe()

acc.dtypes

#Overall Conversion rate and build pie chart
plt.pie(att['Converted to paid customer'].value_counts()/att.shape[0],autopct='%1.1f%%')

#Conversion rate for customer who opted chatbot
plt.pie(att[att['Activate chat bot'] == 'Y']['Converted to paid customer'].value_counts()/att[att['Activate chat bot'] == 'Y'].shape[0],autopct='%1.1f%%')

#Converstion rate by account type
plt.pie(att[att['Converted to paid customer']==1].groupby('Acct type')['Converted to paid customer'].count()/att.groupby('Acct type')['Converted to paid customer'].count(),autopct='%1.1f%%')
print(att[att['Converted to paid customer']==1].groupby('Acct type')['Converted to paid customer'].count())
print(att.groupby('Acct type')['Converted to paid customer'].count())

#converting date time column to Date format
acc['Date time'] = pd.to_datetime(acc['Date time'])

acc.head(5)

#Avg number of clicks by account id
grp_acc = round(acc.groupby('Acct id')['Number of link clicks'].mean(),0)
grp_acc.head(5)

#Left join grp_acct with att
df = pd.merge(att, grp_acc, on = 'Acct id', how = 'left')
df.head(5)

#Encoding account type and Activate chat bot
le = LabelEncoder()
df['Label_Acc_type'] = le.fit_transform(df['Acct type'])
df['Label_chat_bot'] = le.fit_transform(df['Activate chat bot'])
df.head(5)

#Checking for Imbalance data
df['Converted to paid customer'].value_counts()/df.shape[0]*100

df1 = df.drop(['Acct id','Acct type','Activate chat bot'],axis = 1)
df1.head(5)

import seaborn as sns
import matplotlib as plt
sns.heatmap(df1.corr(),cmap = 'coolwarm',annot = True)

X = df1.drop(['Converted to paid customer'],axis = 1)
Y = df1['Converted to paid customer']
print(X.shape)
print(Y.shape)

#Split the data into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state= 123)
print('X train shape :',X_train.shape, 'X test shape :',X_test.shape, 'Y train Shape :',Y_train.shape, 'Y test shape :',Y_test.shape)

model = XGBClassifier()
model.fit(X_train, Y_train)

# Define the hyperparameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 4, 5],
    'learning_rate': [0.1, 0.05, 0.01],
    'subsample': [0.8, 0.9, 1.0],
    'colsample_bytree': [0.8, 0.9, 1.0]
}

#create a grid search object
from sklearn.model_selection import GridSearchCV
grid_search = GridSearchCV(estimator= model, param_grid=param_grid, cv = 3, scoring = 'accuracy')

grid_search.fit(X_train, Y_train)

#Get the best param
param = grid_search.best_params_
print(param)
best_model = grid_search.best_estimator_
print(best_model)

y_pred1 = best_model.predict(X_test)

y_pred = model.predict(X_test)

accuracy = accuracy_score(Y_test, y_pred1)
print("Accuracy :", accuracy)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
cm = confusion_matrix(Y_test, y_pred1)
disp = ConfusionMatrixDisplay(cm, display_labels = model.classes_)
disp.plot()

from sklearn.metrics import f1_score
f1 = f1_score(Y_test, y_pred1)
print("F1 Score :",f1)

from sklearn.linear_model import LogisticRegression

# Create and train the Logistic Regression model
logistic_model = LogisticRegression()
logistic_model.fit(X_train, Y_train)

# Make predictions on the test set
y_pred_logistic = logistic_model.predict(X_test)

# Evaluate the model
accuracy_logistic = accuracy_score(Y_test, y_pred_logistic)
print("Logistic Regression Accuracy:", accuracy_logistic)

f1_logistic = f1_score(Y_test, y_pred_logistic)
print("Logistic Regression F1 Score:", f1_logistic)

cm_logistic = confusion_matrix(Y_test, y_pred_logistic)
disp_logistic = ConfusionMatrixDisplay(cm_logistic, display_labels=logistic_model.classes_)
disp_logistic.plot()

coef = logistic_model.coef_[0]

coef

X.columns

for feature, coefficient in zip(X.columns, coef):
    print(f"{feature}: {np.exp(coefficient)}")

# Find the optimal threshold based on the ROC curve
optimal_idx = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_idx]

print("Optimal Threshold:", optimal_threshold)

# Define your desired threshold
new_threshold = 0.57

# Regenerate predictions based on the new threshold
y_pred_logistic_new = (y_pred_proba_logistic > new_threshold).astype(int)

# Evaluate the model with the new predictions
accuracy_logistic_new = accuracy_score(Y_test, y_pred_logistic_new)
print("Logistic Regression Accuracy with new threshold:", accuracy_logistic_new)

f1_logistic_new = f1_score(Y_test, y_pred_logistic_new)
print("Logistic Regression F1 Score with new threshold:", f1_logistic_new)

cm_logistic_new = confusion_matrix(Y_test, y_pred_logistic_new)
disp_logistic_new = ConfusionMatrixDisplay(cm_logistic_new, display_labels=logistic_model.classes_)
disp_logistic_new.plot()