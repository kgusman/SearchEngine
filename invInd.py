from nltk import word_tokenize
import collections
from nltk.stem import WordNetLemmatizer
import glob, os
from configs import documents_dir

# wordnet_lemmatizer = WordNetLemmatizer()
# inverted_index = collections.defaultdict(set)
#
# test_string = 'Hello. We are test strings which should be tokenized'
# res = word_tokenize(test_string)
# res_lemma = []
# for word in res:
#     res_lemma.append(wordnet_lemmatizer.lemmatize(word, pos='v'))
#
#
# print(res)
# print(res_lemma)

for root, dirs, files in os.walk(documents_dir):
    for file in files:
        if file.endswith(".txt"):
             print(os.path.join(root, file))