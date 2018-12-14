import re;
import math;

categories = []
normal = []
counts = []
vocab = set()


# In[37]:

'''This function normalizes the string passed by removing spaces, numbering, tabs,
newline characters, punctuation marks etc'''

def trimmer(s):
    top = s.strip('\n');
    result = ''.join([i for i in top if not i.isdigit()])
    fin = result.replace(".", "", 1).strip('\t')
    fin = fin.lower()
    fin = re.sub(r'[^\w\s]','',fin)
    return fin

def reader(filename):
    with open(filename) as trial:
        listed = trial.readlines();
        return listed

reader('Questions.txt')



