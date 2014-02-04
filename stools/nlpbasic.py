from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from gensim import corpora, models, utils

class MyLdaModel(models.ldamodel.LdaModel):
    def __getitem__(self, bow, eps=0.01):
        is_corpus, corpus = utils.is_corpus(bow)
        if is_corpus:
            return self._apply(corpus)

        gamma, _ = self.inference([bow])
        topic_dist = gamma[0] / sum(gamma[0]) # normalize to proper distribution
        return [topicvalue for topicid, topicvalue in enumerate(topic_dist)]
                # FIXME: if topicvalue >= eps]

def lda(corpus, dictionary, num_topics):
    model_lda = MyLdaModel(corpus, id2word=dictionary, num_topics=num_topics)
    corpus_lda = model_lda[corpus]
    return corpus_lda

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

def dictionary(stemmed_list):
    dictionary = corpora.Dictionary(stemmed_list)
    return dictionary

def corpus(stemmed_list, dictionary):
    corpus = [dictionary.doc2bow(stemmed) for stemmed in stemmed_list]
    return corpus