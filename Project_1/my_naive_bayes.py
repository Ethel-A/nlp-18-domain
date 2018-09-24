#!/usr/bin/env python
# coding: utf-8

# In[36]:


import re;
import math;

categories = []
normal = []
counts = []
vocab = set()


# In[37]:


'''This function calculates and returns the list of sentences labeled positive and negative respectively'''
def categorize(filename):
    with open(filename) as train_data:
        train_list = train_data.readlines();
        positive = [];
        negative = [];
        #try:
        for item in train_list:
            feat = item.strip('\n');
            if(feat[-1] == '0'): #The statement is a negative
                negative.append(feat[:-2]);
            elif(feat[-1] == '1'):#The statement is a positive
                positive.append(feat[:-2]);
            else:
                print( feat + ": " + feat[-1] + 'Error in data');
                return;
        return(positive, negative)


# In[38]:


'''This function normalizes (takes out punctuations and converts into lowercase all the words in the positive and negative class respectively'''
def normalize(positive,negative):
    pos = positive;
    neg = negative;
    pos_words = [];
    neg_words = [];
    for sentence in pos:
        checked = re.sub(r'[^\w\s]','',sentence) # removing all punctuations except hyphens
        checked = checked.lower();
        x = checked.split(' ');
        for word in x:
            pos_words.append(word);
    for sentence in neg:
        checked = re.sub(r'[^\w\s]','',sentence) # removing all punctuations except hyphens
        checked = checked.lower();
        y = checked.split(' ');
        for word in y:
            neg_words.append(word);
    return pos_words,neg_words
    


# In[39]:


'''This function creates and returns a dictionary with the words/features as keys and their frequency as values for each class'''
def count(pos_words, neg_words):
    pos_dict = {};
    neg_dict = {};
    pos = pos_words;
    neg = neg_words;
    for word in pos:
        if word not in pos_dict:
            pos_dict[word] = 1;
        else:
            pos_dict[word]+=1

    for word in neg:
        if word not in neg_dict:
            neg_dict[word] = 1;
        else:
            neg_dict[word]+=1;

    return pos_dict, neg_dict;


# In[40]:


'''this function combines and returns a set (unique) of all the words in both the positive and negative class'''
def vocabularize(pos_dict, neg_dict):
    pos_count = pos_dict;
    neg_count = neg_dict;
    vocabulary = set();
    for word in pos_count:
        vocabulary.add(word);
    for word in neg_count:
        vocabulary.add(word);
    return vocabulary;


# In[41]:


'''this function normalizes (no punctuation and all lowercase) the test input before testing'''
def test_normalizer(filename):
    with open(filename) as test_data:
        test_list = test_data.readlines();
        stripped_list = [];
        for item in test_list:
            splitz = ' '.join(item.split());
            stripped_list.append(splitz); #for working on normal datasets (unlabelled)
            #stripped_list.append(splitz[:-2]); #for working on labeled datasets
        #return stripped_list;
        normalized = [];
        for sentence in stripped_list:
            checked = re.sub(r'[^\w\s]','',sentence) # removing all punctuations except hyphens
            checked = checked.lower();
            normalized.append(checked);
        return normalized;


# In[42]:


'''The function below initializes the values for the global variables. it is the only function that modifies the variables.
all other function just read the variables'''
def initialize(filename):
    global categories
    global normal
    global counts
    global vocab
    categories = categorize(filename);#returns 2 lists- positive and negative sentences
    normal = normalize(categories[0], categories[1]);   #returns normalized lists of words
    counts = count(normal[0], normal[1]); # returns positive and negative dictionaries
    vocab = vocabularize(counts[0], counts[1]);


# In[43]:


'''This function calculates and returns the prior probability of both the positive and negative class'''    
def prior():
    pos_total = len(categories[0]) # length of positve sentences list
    neg_total = len(categories[1]) # length of negative sentences list
    pos_prob = pos_total/(pos_total + neg_total) # probability of the positive class
    neg_prob = neg_total/(pos_total + neg_total) # probability of the negative class
    return pos_prob, neg_prob;


# In[44]:


'''This function calculates and returns the denominator of the likelihood probability of both the positive and negative class'''
def like_deno():
    vocab_len = len(vocab);
    #print("Vocab Length: '" + str(vocab_len));
    pos_len = 0;
    neg_len = 0;
    pos_freq = list(counts[0].values())
    neg_freq = list(counts[1].values())
    for freq in pos_freq:
        pos_len += freq
    for freq in neg_freq:
        neg_len += freq;
    #print("Positive length: " + str(pos_len))
    #print("Negative lenght: " + str(neg_len))
    pos_deno = vocab_len + pos_len
    neg_deno = vocab_len + neg_len
    return pos_deno, neg_deno;


# In[45]:


'''The function below calculates a list of probabilities of each sentence given the positive class. takes in a normlaized test'''
def pos_tester(test):
    #test = test_normalizer(filename);
    priors = prior();
    pos_prior = priors[0];
    denos = like_deno();
    pos_deno = denos[0];
    pos_count = counts[0];
    pos_probs = [];
    for doc in test:
        cumm = 1;
        test = doc.split(' ');
        for word in test:
            if (word in vocab and word in pos_count) :
                freq = pos_count[word] + 1
            elif(word in vocab):
                freq = 1;
            else:
                continue;
            cumm *= (freq/pos_deno);
        cumm *= pos_prior;
        pos_probs.append(cumm);
        #print(cumm);
    return pos_probs;


# In[46]:


'''The function below calculates a list of probabilities of each sentence given the positive class. takes in a normlaized test'''
def neg_tester(test):
    #test = test_normalizer(test);
    priors = prior();
    neg_prior = priors[1];
    denos = like_deno();
    neg_deno = denos[1]
    neg_count = counts[1];
    neg_probs = [];
    for doc in test:
        cumm = 1;
        test = doc.split(' ');
        for word in test:
            if (word in vocab and word in neg_count) :
                freq = neg_count[word] + 1
            elif(word in vocab):
                freq = 1;
            else:
                continue;
            cumm *= (freq/neg_deno);
        cumm *= neg_prior;
        neg_probs.append(cumm);
        #print(cumm);
    return neg_probs;


# In[47]:


'''The function below calculates and returns the estimated class of the various sentences in the test file'''
def tester(filename):
    test = test_normalizer(filename);
    positives = pos_tester(test)
    negatives = neg_tester(test)
    results_file = open('results_file.txt','w+')
    results = []
    for i in range(len(positives)):
        if positives[i] > negatives[i]:
            results_file.write('1' + '\n');
            results.append('Positive')
        elif positives[i] < negatives[i]:
            results.append('Negative')
            results_file.write('0' + '\n');
        else:
            results.append('neutral');
    results_file.close();
    return results;


# In[48]:


'''Master function'''
def boss(trainfile, testfile):
    initialize(trainfile);
    return tester(testfile);


# In[50]:


name = input("Enter file name: ")
boss('bigTrain.txt',name);

