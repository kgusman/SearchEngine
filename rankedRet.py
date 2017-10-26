from invInd import *
import time
from math import log10, sqrt
from search import get_doc_by_name
from itertools import islice
from operator import itemgetter

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

""" Create idf of all documents of the corpus """
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

""" Create tf vector """
def create_tf(words):
    tf = {}
    for word in words:
        tf.setdefault(word, 0)
        tf[word] += 1
    tf_wt = []
    for elem in tf:
        tf_wt.append(round(1 + log10(float(tf[elem])), 2))

    return tf_wt

""" Create tf vector with words from query """
def create_tf_doc(query, document):
    tf = {}
    for word in document:
        tf.setdefault(word, 0)
        tf[word] += 1
    tf_wt = []
    for word in query:
        if word in tf:
            tf_wt.append(round(1 + log10(float(tf[word])), 2))
        else:
            tf_wt.append(0)

    return tf_wt

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

""" Cosine normalization """
def normalization_vector(vector):
    normalized = []
    n = norm(vector) # norm of the vector
    for elem in vector:
        normalized.append(elem/n)
    return normalized

""" Create vector of a query with normalization"""
def ltc_query(tf_query, idf):
    idf_query = []
    for elem in idf:
        idf_query.append(idf[elem][0])

    tf_idf = []
    for i in range(len(tf_query)):
        tf_idf.append(tf_query[i] * idf_query[i])
    return normalization_vector(tf_idf)

""" Create vector of a document with normalization """
def lnc_document(query, document):
    ln = create_tf_doc(query, document)
    lnt = normalization_vector(ln)

    return lnt

""" Get documents which contatin words of the query """
def get_documents_of_query(query, idf):
    docs = []
    for word in query:
        if word in idf:
            for doc in idf[word][1]:
                if doc not in docs:
                    docs.append(doc)

    return docs

def calculate_lnc_ltc(lnc, ltc):
    assert len(lnc) == len(ltc), 'length of lnc and ltc is not the same'
    return dot_product(lnc, ltc)

def get_scores(query, docs, ltc):
    scores = {}
    for doc in docs:
        lnc = lnc_document(query, parse_abstract(get_doc_by_name(doc)))
        lnc_ltc = calculate_lnc_ltc(lnc, ltc)
        scores[doc] = round(lnc_ltc, 2)

    return scores

def take(n, iterable):
    return list(islice(iterable, n))

def search(query, K):
    query = query.split()
    words_query = lemmatize(query)
    idf = create_idf()
    ltc = ltc_query(create_tf(words_query), idf)
    docs = get_documents_of_query(words_query, idf)
    scores = get_scores(words_query, docs, ltc)
    # TODO: print TOP 20 document with scores

    # sort scores by value
    sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)
    top_K = take(K, sorted_scores)
    return top_K

