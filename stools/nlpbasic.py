from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

def tokenize(doc):
    tokenizer = RegexpTokenizer(r'\w+')
    token_list = tokenizer.tokenize(doc)
    return token_list

def remove_stop_word(word_list):
    stop = stopwords.words('english')
    removed = [i for i in word_list if i not in stop]
    return removed

def stem(word_list):
    stemmer = LancasterStemmer()
    stemmed = [stemmer.stem(i) for i in word_list]
    return stemmed

def trs(doc):
    token_list = tokenize(doc)
    removed = remove_stop_word(token_list)
    stemmed = stem(removed)
    return stemmed