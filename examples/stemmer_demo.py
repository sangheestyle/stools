import sys
sys.path.append("..")
from stools.stemmer import Stemmer

# Stemmer requires only word to stem it
text = "game is kind of * Ringtone andrOid love support, server mobile differently twitter please."
words = text.split()

lancaster_stemmer = Stemmer().create_stemmer("lancaster")
porter_stemmer = Stemmer().create_stemmer("porter")
snowball_stemmer = Stemmer().create_stemmer("snowball")

for word in words:
    print "==origin : " + word
    print "lancaster: " + lancaster_stemmer.stem(word)
    print "porter   : " + porter_stemmer.stem(word)
    print "snowball : " + snowball_stemmer.stem(word)
    print ""