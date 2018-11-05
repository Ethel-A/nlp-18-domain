#Using the sciKit learn naive Bayes library.

'''Importing Libraries and Loading Datasets'''
from sklearn import datasets; #imports datasets that will be used to test the classifier
from sklearn import metrics; #imports the evaluation metrics that will be used to compare the classifiers
from sklearn.naive_bayes import GaussianNB; #imports that Gaussian Naive Bayes Classifier - which is a naive bayes classifier that works on the assumption that the distribution is Gaussian (normal)

dataset = datasets.load_iris(); # loads the iris dataset - which is a class sytem for iris plants

'''Creating Naive-Bayes Classifier'''
model = GaussianNB();#creates a model that works on the assumption that the distribution is gaussian
model.fit(dataset.data, dataset.target); #fits the model to the dataset

'''Making Predictions'''
expected = dataset.target;
predicted = model.predict(dataset.data);#returns the predicted values of the iris dataset

'''Testing Accuracy and statisitics on dataset'''
print(metrics.classification_report(expected,predicted));
print(metrics.confusion_matrix(expected,predicted));

#PROGRAM WORKS - NEXT STEP: CHANGE DATASET FOR SENTIMENT CLASSIFICATION
