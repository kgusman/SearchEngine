from invInd import *
import time
from math import log10, sqrt

def open_docs_in_directories(type):
    docs = []
    documents_dir = get_docs(type)
    length = 0
    for root, dirs, files in os.walk(documents_dir):
        for file in files:
            if file.endswith(".txt"):
                 docs.append(os.path.join(root, file))
                 length += 1
    return docs, length

def create_idf(type=1):
    start_time = time.time()
    df = {}
    docs_list, N = open_docs_in_directories(type)
    for doc in docs_list:
        lemma_words = parse_abstract(doc)
        if lemma_words != None:
            for word in list(lemma_words):
                df.setdefault(word, [0, []])
                temp = doc.split('/')
                if (temp[len(temp) - 1] not in df[word][1]):
                    df[word][0] += 1
                    df[word][1].append(temp[len(temp) - 1])
    est_time = time.time() - start_time
    print("idf created in %d seconds." %(est_time))
    for elem in df:
        df[elem][0] = round(log10(float(N)/float(df[elem][0])), 2)
    return df

""" Calculate dor product """
def dot_product(K, L):
   if len(K) != len(L):
      return 0
   return sum(i[0] * i[1] for i in zip(K, L))

""" Calculate norm of a vector """
def norm(vec):
    n = 0
    for elem in vec:
        n += elem**2
    return sqrt(n)

""" Calculate cosine similarity """
def cosine_similarity(query, doc):
    dot = dot_product(query, doc)
    query_norm = norm(query)
    doc_norm = norm(doc)

    return dot/(query_norm*doc_norm)

def check():
    df = create_idf()

