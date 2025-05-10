import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

data = pd.read_csv('alzheimers_disease_data.csv')

features = data.drop(['Diagnosis', 'PatientID','DoctorInCharge'], axis=1)  
target = data['Diagnosis']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42, stratify=target)

model = GaussianNB()  # simple default value
model.fit(X_train, y_train)

y_predict = model.predict(X_test)
trainscore = model.score(X_train, y_train)
testscore = model.score(X_test, y_test)

print("Accuracy: {:.2f}%".format(testscore * 100))