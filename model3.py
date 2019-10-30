import math
import os
import re
import glob
import operator
import pandas as pd
import numpy as np

"""GLOBAL VARIABLES"""
chi_squares = []
ham_data = []
spam_data = []
ham_data_pr = {}
spam_data_pr = {}
chi_square_dict = {}
sorted_chi_square_dict = {}


ham_test = []
spam_test = []




"""READING, NORMALIZING, TOKENIZING"""
def reader(dir):
    ham_files = glob.glob(dir+"/*msg?.txt")
    spam_files = glob.glob(dir+"/spms*.txt")

    ham_dictionary = {file: tokenizer(open(file).read()) for file in ham_files} # make a dictionary of all ham files
    ham_tokens = ham_dictionary.values()
    for ham_token in ham_tokens:
        for e in ham_token:
            ham_data.append(e)

    spam_dictionary = {file: tokenizer(open(file).read()) for file in spam_files} # make a dictionary of all ham files
    spam_tokens = spam_dictionary.values()
    for spam_token in spam_tokens:
        for e in spam_token:
            spam_data.append(e)

    return ham_data, spam_data

def normalise(word):
    return re.sub(r'\W+', '', word.lower())

def tokenizer(str):
    tokens = [normalise(word) for word in str.split(" ") if normalise(word).isalpha()]
    allTokens = tokens
    return allTokens

"""UNIQUE WORDS"""

def UniqueWordsMaker():
    print "=== spam_data: " + str(len(spam_data)) + " ==="
    for word in spam_data:
        if word not in spam_data_pr.keys():
            spam_data_pr.update({word:1})

        if word in spam_data_pr.keys():
            value = spam_data_pr.get(word) + 1
            spam_data_pr.update({word: value})

    print "=== ham_data: " + str(len(ham_data)) + " ==="

    for word in ham_data:
        if word not in ham_data_pr.keys():
            ham_data_pr.update({word:1})

        if word in ham_data_pr.keys():
            value = ham_data_pr.get(word) + 1
            ham_data_pr.update({word: value})

"""TRAINING"""


"""BUILDING CHI SQUARE LIST"""

def chi_square():
    print "chi square calculations starting..."
    #data = np.array([ham_data_pr.keys(), "h",0])
    spam_data_pd = pd.DataFrame(columns=["data", "n_words", 'chi_score', "label" ])
    spam_data_pd["data"] = spam_data_pr.keys()
    spam_data_pd["label"] = "s"
    spam_data_pd["chi_score"] = 0
    spam_data_pd["n_words"] = spam_data_pr.values()

    ham_data_pd = pd.DataFrame(columns=["data", "n_words", 'chi_score', "label" ])
    ham_data_pd["data"] = ham_data_pr.keys()
    ham_data_pd["label"] = "h"
    ham_data_pd["chi_score"] = 0
    ham_data_pd["n_words"] = ham_data_pr.values()
    data = spam_data_pd.append(ham_data_pd)


    n_ham_data = len(data[data['label']=="h"])
    n_spam_data = len(data[data['label']=="s"])
    data['1_1'] = np.where(data["data"].isin(data[data['label']=="h"]["data"]),data["n_words"],0)
    data['1_2'] = np.where(data["data"].isin(data[data['label']=="s"]["data"]),data["n_words"],0)
    data['2_1'] = n_ham_data - data['1_1']
    data['2_2'] = n_ham_data - data['1_2']
    data['C1'] = data['1_1'] + data['2_1']
    data['C2'] = data['1_2'] + data['2_2']
    data['W1'] = data['1_1'] + data['1_2']
    data['W2'] = data['2_1'] + data['2_2']
    data['N'] = data['C1'] + data['C2']
    data['E1_1'] = (data['W1'] * data['C1']) / data['N']
    data['E1_2'] = (data['W1'] * data['C2']) / data['N']
    data['E2_1'] = (data['W2'] * data['C1']) / data['N']
    data['E2_2'] = (data['W2'] * data['C2']) / data['N']
    #chi_square_score = sum(((M[i,j] - E[i,j]) ** 2) / E[i, j] for i in range(1, 3) for j in range(1, 3) if E[i, j] > 0)

    cols = ['1_1','1_2','2_1','2_2']
    cols2 = ['E1_1','E1_2','E2_1','E2_2']
    data['chi_score'] = sum(((data[c] - data[e])**2)/data[e] for c in cols for e in cols2)

    data = data.sort_values(by=["chi_score"], ascending=False)

    data = data.reset_index()
    return data

def read_data(dir):
    ham_files = glob.glob(dir+"/*msg?.txt")
    spam_files = glob.glob(dir+"/spms*.txt")
    ham_dictionary = {file.split("/")[-1]: tokenizer(open(file).read()) for file in ham_files}
    spam_dictionary = {file.split("/")[-1]: tokenizer(open(file).read()) for file in spam_files}

    return ham_dictionary, spam_dictionary

def probability_word(word, hamspam):
    if hamspam == "h":
        dict = ham_dictionary
    else:
        dict = spam_dictionary
    i = 0
    for doc in dict:
        if word in dict[doc]:
            i += 1


    result = (float(i + 1) / float(len(dict) + 2))
    return result

def doc_probability(doc):
    doc = tokenizer(open(dir + doc).read())
    result_ham = float(len(ham_dictionary))/float(len(ham_dictionary) + len(spam_dictionary))
    result_spam = float(len(spam_dictionary))/float(len(ham_dictionary) + len(spam_dictionary))

    for word in doc:
        #print data_300[data_300["label"]=="s"]['data'].to_list()
        if word in data_300[data_300["label"]=="h"]['data'].to_list():
            print probability_word(word, "h")
            result_ham = result_ham*probability_word(word, "h")
        if word in data_300[data_300["label"]=="s"]['data'].to_list():
            print word
            result_spam = result_spam*probability_word(word, "s")

    if result_ham > result_spam:
        return "ham", result_ham
    else:
        return "spam", result_spam

if __name__ == "__main__":
    dir = "/Users/amydelange/Documents/corpus-mails/corpus/Emails2/"
    ham_dictionary,spam_dictionary =  read_data(dir)


    """DIRECTORIES"""


    trainCorpus = reader(dir) #getting train corpus files from computer
    #testCorpus = reader("/Users/amydelange/Documents/corpus-mails/corpus/part10") #getting test corpus files from computer


    print "=== Start UniqueWordsMaker ==="
    UniqueWordsMaker()

    print "=== Start chi_square"

    data = chi_square()
    data_100 = data[data.index<100]
    data_200 = data[data.index<200]
    data_300 = data[data.index<300]

    for file in os.listdir(dir):
        print doc_probability(file)
