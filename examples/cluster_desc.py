import os
import multiprocessing
from subprocess import call
import cld
from stools import io, nlpbasic, ml
from numpy import array

folder_path = "data_google_play"
json_names = [['extendedInfo', 'description']]
if not os.path.exists(folder_path):
    call(["git", "clone", "https://github.com/sangheestyle/data_google_play.git"])

json_contents, file_names = io.read_json_folder(folder_path, '.json', json_names)
descriptions = zip(*json_contents)[0]
name_desc_pairs = {}
for idx, desc in enumerate(descriptions):
    if len(desc) > 1000:
        lang = cld.detect(desc.encode('utf-8'))
        if lang[1] == 'en' and len(lang[4]) == 1:
            name_desc_pairs[file_names[idx]] = desc.encode('ascii', errors='ignore')

documents = name_desc_pairs.values()
pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
stemmed_list = pool.map(nlpbasic.trs, documents)
dictionary = nlpbasic.dictionary(stemmed_list)
corpus = nlpbasic.corpus(stemmed_list, dictionary)
corpus_lda = nlpbasic.lda(corpus, dictionary, num_topics=5)

vectors = [array(f) for f in corpus_lda]
ml.KMeans(vectors, n_clusters=5, max_iter=1000)