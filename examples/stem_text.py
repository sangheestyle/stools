import sys
sys.path.append("..")
from stools.nlp import stem_text

if __name__ == "__main__":
    stemmer_name, input_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    stem_text(stemmer_name, input_file, output_file)
