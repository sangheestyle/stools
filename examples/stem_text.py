import sys
sys.path.append("..")
from stools.stemmer import Stemmer
from stools import nlp

def main():
    stemmer_type, input_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(input_file, "r") as f:
        text = f.read()
    words = nlp.tokenize(text)
    stemmer = Stemmer().create_stemmer(stemmer_type)
    stemming_result = []
    for word in words:
        stemming_result.append(stemmer.stem(word))
    with open(output_file, "w") as f:
        f.write(' '.join(stemming_result))

if __name__ == "__main__":
    main()