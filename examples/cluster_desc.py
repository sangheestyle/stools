import os
import sys
from subprocess import call
from operator import itemgetter
from itertools import groupby
from collections import Counter
import cld
from numpy import array
from sklearn.feature_extraction.text import CountVectorizer
sys.path.append("..")
from stools import stio, nlp, ml
from stools.wordcloud.wordcloud import make_wordcloud

folder_path = "data_google_play"
json_names = [['extendedInfo', 'description']]
if not os.path.exists(folder_path):
    call(["git", "clone", "https://github.com/sangheestyle/data_google_play.git"])

json_contents, file_names = stio.read_json_folder(folder_path, '.json', json_names)
descriptions = zip(*json_contents)[0]

# The number of input files is 1365, but the number of result of apk_info
# is 971 due to flitering by length of description and language (english only)
apk_info = []
for idx, desc in enumerate(descriptions):
    if len(desc) > 1000:
        lang = cld.detect(desc.encode('utf-8'))
        if lang[1] == 'en' and len(lang[4]) == 1:
            apk_info.append([file_names[idx], desc.encode('ascii', errors='ignore')])

filtered_desc = zip(*apk_info)[1]
stemmed_list = nlp.trs(filtered_desc, "snowball")
dictionary = nlp.dictionary(stemmed_list)
corpus = nlp.corpus(stemmed_list, dictionary)
corpus_lda = nlp.lda(corpus, dictionary, num_topics=5)

vectors = [array(f) for f in corpus_lda]
prediction = ml.KMeans(vectors, n_clusters=5, max_iter=1000)
for idx, item in enumerate(apk_info):
    apk_name = item[0]
    stemmed_content = ' '.join(stemmed_list[idx])
    groupID = prediction[idx]
    apk_info[idx] = [apk_name, stemmed_content, groupID]

apk_info.sort(key = itemgetter(2))
groups = groupby(apk_info, itemgetter(2))
desc_groups = [[item[1] for item in data] for key, data in groups]

for idx, contents_list in enumerate(desc_groups):
    file_name = "cluster_" + str(idx) + ".txt"
    text = ' '.join(array(contents_list).flatten())
    with open(file_name, "w") as f:
        f.write("%s" % text)
    occurrences = Counter(text.split())
    words = array(occurrences.keys())
    counts = array(occurrences.values())
    words = words[counts > 1]
    counts = counts[counts > 1]
    output_pic_file_name = "cluster_" + str(idx) + ".png"
    make_wordcloud(words, counts, output_pic_file_name,
                   font_path="../stools/wordcloud/font/DroidSansMono.ttf")
