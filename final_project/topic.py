# -*- coding: utf-8 -*-
"""topic

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g1KDA3BuKYLi8TMGBwl76zwHBq4nm26x
"""

from google.colab import files
uploaded = files.upload()

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

def trimmer(s):
    top = s.strip('\n');
    result = ''.join([i for i in top if not i.isdigit()])
    fin = result.replace(".", "", 1).strip('\t')
    fin = fin.lower()
    fin = re.sub(r'[^\w\s]','',fin)
    fin = fin.strip(' ')
    return fin

import re

def listed(filename):
  trimmed = []
  with open (filename) as loaded:
    listed = loaded.readlines()
    for line in listed:
      if line != "":
        stripped = trimmer(line)
        trimmed.append(stripped)
      else:
        continue
    return trimmed

#print(listed('Questions.txt'))

def labeler(topics):
  topic_set = set()
  label = 0
  for line in topics:
    topic_set.add(line)
  topic_dict = {}
  for item in topic_set:
    topic_dict[item] = label
    label = label + 1
  labels = []
  for line in topics:
    val = topic_dict[line]
    labels.append(val)
  return labels

# labels = labeler(listed('Topics.txt'))
# for i in range(len(topics)):
#   print(str(topics[i]) + ": " + str(labels[i]))

def topic_generator(test_file):
  topics = listed('Topics.txt')
  questions = listed('Questions.txt')

  questions = questions[:-5]


  tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
  features = tfidf.fit_transform(questions).toarray()

  X_train, X_test, y_train, y_test = train_test_split(questions, topics, random_state = 0)
  count_vect = CountVectorizer()
  X_train_counts = count_vect.fit_transform(X_train)
  tfidf_transformer = TfidfTransformer()
  X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
  model = MultinomialNB().fit(X_train_tfidf, y_train)
 
  test = listed(test_file)
  results = open("topic_results.txt","w+")
  for line in test:
    quest = count_vect.transform([line])
    ans = model.predict(quest)[0]
    results.write(ans)
    results.write('\n')
  results.close()
#   question = 'How many regions are in Ghana'
  
#   return ans

#topic_generator('Questions.txt')



qna_generator('Questions.txt')