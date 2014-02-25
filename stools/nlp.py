from multiprocessing import Pool, cpu_count
from functools import partial
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from gensim import corpora, models, utils
from stools.stemmer import Stemmer

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

def stem(stemmer_name, word_list):
    stemmer = Stemmer().create_stemmer(stemmer_name)
    stemmed = [stemmer.stem(i) for i in word_list]
    return stemmed

def stem_text(stemmer_name, input_file, output_file=None):
    with open(input_file, "r") as f:
        contents = [line.strip() for line in f]
    stemmed_doc_list = trs(contents, stemmer_name)
    if output_file == None:
        return stemmed_doc_list
    else:
        with open(output_file, "w") as f:
            for doc_list in stemmed_doc_list:
                for item in doc_list:
                    f.write("%s " % item)

def trs(contents, stemmer_name="lancaster"):
    if type(contents) == list or tuple:
        pool = Pool(processes=cpu_count())
        stemmed_doc_list = pool.map(partial(trs_job, stemmer_name=stemmer_name),
                                    contents)
        return stemmed_doc_list
    elif type(contents) == str:
        stemmed_doc = trs_job(contents)
        return stemmed_doc
    else:
        raise ValueError

def trs_job(doc, stemmer_name="lancaster"):
    token_list = tokenize(doc)
    removed = remove_stop_word(token_list)
    stemmed = stem(stemmer_name, removed)
    return stemmed

def dictionary(stemmed_list):
    dictionary = corpora.Dictionary(stemmed_list)
    return dictionary

def corpus(stemmed_list, dictionary):
    corpus = [dictionary.doc2bow(stemmed) for stemmed in stemmed_list]
    return corpus
