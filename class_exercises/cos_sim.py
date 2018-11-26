#This function compares the similarities of 2 sentences or documents using cosine similarities, suitable for QandAs and Topic Modeling

import numpy as np

# sentences
s = ["How many teams participated in the first world cup?", "Who holds the record for top scorer in a single World Cup?", "Should I sell my car myself or trade it in?",
"How important is car maintenance?", "How much does AWS SAM cost to use","Which languages does AWS SAM support" ]

# a = "How many teams participated in the first world cup?"
# b = "Who holds the record for top scorer in a single World Cup?" 
# c = "Should I sell my car myself or trade it in?"
# d = "How important is car maintenance?"
# e = "How much does AWS SAM cost to use"
# f = "Which languages does AWS SAM support"
def tokenize(s):
    words = [];
    sentences = []
    for line in s:
        split = line.split(' ');
        sentences.append(split)
        for x in split:
            words.append(x);
    return words, sentences;

def counter(s):
    vectors = []
    bow = tokenize(s)[0];
    sentence = tokenize(s)[1];
    for sent in sentence:
        vector = []
        for word in bow:
            if word in sent:
                vector.append(1)
            else:
                vector.append(0)
        vectors.append(vector)
    return vectors         
        
        
        

def cos_sim(s):
    vectors = counter(s)
    #print(vectors)
    for a in vectors:
        
        for b in vectors:
            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            ans = round(dot_product / (norm_a * norm_b),2)
            print (str(ans), end = "\t")
        print('\n')
            
cos_sim(s)

