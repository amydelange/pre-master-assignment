import math
import os
import re

def reader(dir, filter):
    files = os.listdir(dir) # list all files in 'dir'
    filteredFiles = [filename for filename in files if filter in filename] # filter all files
    dictionary = {file: tokenizer(open(dir + "/" + file).read()) for file in filteredFiles} # make a dictionary of all files
    return dictionary

def normalise(word):
    return re.sub(r'\W+', '', word.lower())

def tokenizer(str):
    tokens = [normalise(word) for word in str.split(" ") if normalise(word).isalpha()]
    return tokens

ham = reader("/Users/amydelange/Documents/corpus-mails/corpus/Emails", "msg") #getting ham files from computer
spam = reader("/Users/amydelange/Documents/corpus-mails/corpus/Emails", "spms") #getting spam files from computer

print "testing"

def estimatedProbability(word, dict):
    divisor = float(sum(word in document for document in dict.values()) + 1)
    numerator = float(len(dict) + 2)
    return (divisor / numerator)

def testDocument(words):
    hamValues = [val for sublist in ham.values() for val in sublist]
    spamValues = [val for sublist in spam.values() for val in sublist]
    document = [word in hamValues or word in spamValues for word in words]
    return document

def probabilityFilter(inDocument, prob):
  if inDocument:
      return prob
  else:
      return 1.0 - prob

def classifySingle(email):
    document = testDocument(email)

    probHam1 = [estimatedProbability(word, ham) for word in email]
    probHam2 = map(probabilityFilter, document, probHam1)
    probHam3 = [float(len(ham))/float(len(ham) + len(spam))] + probHam2
    probHam4 = reduce(lambda x, y: x * y, probHam3)

    probSpam1 = [estimatedProbability(word, spam) for word in email]
    probSpam2 = map(probabilityFilter, document, probSpam1)
    probSpam3 = [float(len(spam))/float(len(ham) + len(spam))] + probSpam2
    probSpam4 = reduce(lambda x, y: x * y, probSpam3)

    return (probHam4, probSpam4, probHam4 <= probSpam4)

def classify_single_logspace(email):
    document = testDocument(email)

    probHam1 = [estimatedProbability(word, ham) for word in email]
    probHam2 = map(probabilityFilter, document, probHam1)
    probHam3 = [float(len(ham))/float(len(ham) + len(spam))] + probHam2
    probHam4 = sum(math.log(val, 2) for val in probHam3)

    probSpam1 = [estimatedProbability(word, spam) for word in email]
    probSpam2 = map(probabilityFilter, document, probSpam1)
    probSpam3 = [float(len(spam))/float(len(ham) + len(spam))] + probSpam2
    probSpam4 = sum(math.log(val, 2) for val in probSpam3)

    return (probHam4, probSpam4, probHam4 <= probSpam4)

print "still testing"

def chi_square(word):
    M = {}
    M[1,1] = sum(int(word in row) for row in ham.values())
    M[1,2] = sum(int(word in row) for row in spam.values())
    M[2,1] = sum(int(word not in row) for row in ham.values())
    M[2,2] = sum(int(word not in row) for row in spam.values())

    C = {}
    C[1] = float(M[1,1] + M[2,1])
    C[2] = float(M[1,2] + M[2,2])

    W = {}
    W[1] = float(M[1,1] + M[1,2])
    W[2] = float(M[2,1] + M[2,2])

    N = float(C[1] + C[2])

    E = {}
    E[1,1] = float(W[1] * C[1]) / N
    E[1,2] = float(W[1] * C[2]) / N
    E[2,1] = float(W[2] * C[1]) / N
    E[2,2] = float(W[2] * C[2]) / N

    result = sum(((M[i,j] - E[i,j]) ** 2) / E[i, j] for i in range(1, 3) for j in range(1, 3) if E[i, j] > 0)
    return result

def filter_highest(email, n):
    uniqueWords = set(email) # get all unique words in the email
    scoredWords = [(chi_square(word), word) for word in uniqueWords] # give every word a score
    scoredWords.sort(reverse = True) # sort the scored words in descending order
    return [word[1] for word in scoredWords[:n]]

def classifyAll(dir):
    files = os.listdir(dir)
    emails = [(file, tokenizer(open(dir + "/" + file).read())) for file in files]

    for email in emails[:3]:
        mostImportantWords = filter_highest(email[1], 100)
        return email[0]
        return classify_single_logspace(mostImportantWords)

print "still testing"

def print_highest_chi_values(dir, n):
    emails = [tokenizer(open(dir + "/" + file).read()) for file in os.listdir(dir)]
    uniqueWords = { word for email in emails for word in email }
    scoredWords = [(chi_square(word), word) for word in uniqueWords] # give every word a score
    scoredWords.sort(reverse = True) # sort the scored words in descending order

    return scoredWords[:n]

classify_single_logspace("/Users/amydelange/Documents/corpus-mails/corpus/part10")


print_highest_chi_values("/Users/amydelange/Documents/corpus-mails/corpus/Emails", 100) #amount of words so this is list of 100 words with highest chi values
