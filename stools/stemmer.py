from nltk.stem import LancasterStemmer, PorterStemmer, snowball

class Stemmer(object):
    def create_stemmer(self, stemmer_name):
        if stemmer_name == "lancaster": return LancasterStemmer()
        elif stemmer_name == "porter": return PorterStemmer()
        elif stemmer_name == "snowball": return snowball.EnglishStemmer()
        else: NotImplementedError