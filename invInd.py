import collections
from nltk.stem import WordNetLemmatizer
from configs import *
from nltk.corpus import stopwords
import re
import os
import time

def lemmatize(words):
    wordnet_lemmatizer = WordNetLemmatizer()
    res_lemma = []
    for word in words:
        word = re.sub(r"([0-9])|(\\)|(\?)|(\/)|(\%)|(\<)|(\>)|(\_)|(\$)|(\-)|(\&)|(\))|(\()|(\+)", "", word)
        res_lemma.append(wordnet_lemmatizer.lemmatize(word))

    return res_lemma

def get_docs(type):
    if type == 1:
        return documents_dir_easy
    elif type == 2:
        return documents_dir_medium
    elif type == 3:
        return documents_dir_hard
    else:
        print("Wrong type of directory.")
        input_type = input("Enter type of a directory (1, 2, 3): ")
        return get_docs(input_type)


def open_docs_in_directories(type):
    docs = []
    documents_dir = get_docs(type)
    for root, dirs, files in os.walk(documents_dir):
        for file in files:
            if file.endswith(".txt"):
                 docs.append(os.path.join(root, file))
    return docs

def parse_abstract(doc_name):
    text = ""
    with open(doc_name, 'r') as f:
        for line in f:
            if line.startswith("Abstract"):
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

    return lemmatize(filtered_words)

def create_inverted_index(type=1):
    start_time = time.time()
    inverted_index = collections.defaultdict(set)
    docs_list = open_docs_in_directories(type)
    for doc in docs_list:
        lemma_words = parse_abstract(doc)
        if lemma_words != None:
            for word in list(lemma_words):
                inverted_index[word].add(doc)
    est_time = time.time() - start_time
    print("Inverted index created in %d seconds." %(est_time))
    return inverted_index
