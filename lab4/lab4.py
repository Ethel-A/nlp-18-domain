from sklearn.feature_extraction.text import CountVectorizer;
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")
    
'''Function to train unormalized data'''
def trainer():
  with open('bigTrain.txt') as train_data:
    train_list = train_data.readlines()
    data = []
    labels = []
  for line in train_list:
    data.append(line[:-3])
    labels.append(line[-2])

  vectorizer = CountVectorizer(lowercase = False)
  
  normFeat = vectorizer.fit_transform(data)
  normFeat = normFeat.toarray() # for easy usage
  X_train, X_test, y_train, y_test  = train_test_split(
          normFeat, 
          labels,
          train_size=0.80, 
          random_state=1234)
  return X_train, X_test, y_train, y_test, vectorizer

def modeler(X_train, y_train):
  log_model = LogisticRegression()
  log_model = log_model.fit(X_train, y_train)
  return log_model

def tester(X_test, model):
  y_pred = model.predict(X_test)
  return y_pred

def main(testfile):
  with open(testfile) as testdata:
      test = testdata.readlines()
  vals = trainer()
  X_train = vals[0]
  X_test = vals[1]
  y_train = vals[2]
  y_test = vals[3]
  vectorizer = vals[4]
  test = vectorizer.fit_transform(test)
  test = test.toarray()
  model = modeler(X_train, y_train)
  predictions = tester(test, model)
  print(predictions)
  
