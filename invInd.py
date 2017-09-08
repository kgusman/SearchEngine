from nltk import word_tokenize
import collections
from nltk.stem import WordNetLemmatizer
import glob, os
from configs import documents_dir
from nltk.corpus import stopwords

def lemmatize(doc_path):
    wordnet_lemmatizer = WordNetLemmatizer()
    inverted_index = collections.defaultdict(set)

    test_string = 'Hello. We are test strings which should be tokenized'
    res = word_tokenize(test_string)
    res_lemma = []
    for word in res:
        res_lemma.append(wordnet_lemmatizer.lemmatize(word, pos='v'))


    print(res)
    print(res_lemma)

def open_docs_in_directories():
    for root, dirs, files in os.walk(documents_dir):
        for file in files:
            if file.endswith(".txt"):
                 print(os.path.join(root, file))


def parse_abstract(doc_name):
    text = ""
    with open(doc_name, 'r') as f:
        for line in f:
            if line.startswith("Abstract    :"):
                for l in f:
                    text += l.lower()

    text = text.replace("%%%", "")
    text = text.replace("***", "")

    """ Split a string to a list of strings """
    text_list = text.split()

    """ If there is no abstract in the document we'll know it """
    if len(text_list) <= 2:
        return None

    """ Abstract can start with this keywords, which we do not need """
    if text_list[0] == 'abstract' or text_list[0].isdigit():
        text_list.remove(text_list[0])
    if text_list[0].isdigit():
        text_list.remove(text_list[0])

    text_list = [s.replace(',', '') for s in text_list]
    text_list = [s.replace('.', '') for s in text_list]
    text_list = [s.replace('"', '') for s in text_list]

    """ Removing stop word from the text """

    filtered_words = [word for word in text_list if word not in stopwords.words('english')]

    print(filtered_words)

# open_docs_in_directories()
# parse_abstract("./Corpus/Part1/awards_1994/awd_1994_96/a9496308.txt")