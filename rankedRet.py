from invInd import *
import time
from math import log10, sqrt
from search import get_doc_by_name
from itertools import islice
from operator import itemgetter

class RankedRetrieval():

    def __init__(self):
        self.idf = None

    def change_type(self):
        type = input("Enter type for an index (0, 1, 2 or 3): ")
        print("Initialize inverted index...")
        if type == str(0):
            self.idf = self.create_idf()
        elif type == str(1):
            self.idf = self.create_idf(1)
        elif type == str(2):
            self.idf = self.create_idf(2)
        elif type == str(3):
            self.idf = self.create_idf(3)
        else:
            print("Wrong type of the index. Start again.")

    def open_docs_in_directories(self, type):
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
    def create_idf(self, type=0):
        start_time = time.time()
        df = {}
        docs_list, N = self.open_docs_in_directories(type)
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
    def create_tf(self, words):
        tf = {}
        for word in words:
            tf.setdefault(word, 0)
            tf[word] += 1
        tf_wt = []
        for elem in tf:
            tf_wt.append(round(1 + log10(float(tf[elem])), 2))
        return tf_wt

    """ Create tf vector with words from query """
    def create_tf_doc(self, query, document):
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

    """ Calculate dot product """
    def dot_product(self, K, L):
       if len(K) != len(L):
          return 0
       return sum(i[0] * i[1] for i in zip(K, L))

    """ Calculate norm of a vector """
    def norm(self, vec):
        n = 0
        for elem in vec:
            n += elem**2
        return sqrt(n)

    """ Calculate cosine similarity """
    def cosine_similarity(self, query, doc):
        dot = self.dot_product(query, doc)
        query_norm = self.norm(query)
        doc_norm = self.norm(doc)
        return dot/(query_norm*doc_norm)

    """ Cosine normalization """
    def normalization_vector(self, vector):
        normalized = []
        n = self.norm(vector) # norm of the vector
        for elem in vector:
            normalized.append(elem/n) # elem is already float type, so we do not need to customize
        return normalized

    """ Create vector of a query with normalization"""
    def ltc_query(self, tf_query):
        idf_query = []
        for elem in self.idf:
            idf_query.append(self.idf[elem][0])

        tf_idf = []
        for i in range(len(tf_query)):
            tf_idf.append(tf_query[i] * idf_query[i])
        return self.normalization_vector(tf_idf)

    """ Create vector of a document with normalization """
    def lnc_document(self, query, document):
        ln = self.create_tf_doc(query, document)
        lnt = self.normalization_vector(ln)

        return lnt

    """ Get documents which contatin words of the query """
    def get_documents_of_query(self, query):
        docs = []
        for word in query:
            if word in self.idf:
                for doc in self.idf[word][1]:
                    if doc not in docs:
                        docs.append(doc)

        return docs

    def calculate_lnc_ltc(self, lnc, ltc):
        assert len(lnc) == len(ltc), 'length of lnc and ltc is not the same'
        return self.dot_product(lnc, ltc)

    """ Get cosine score for query-docs """
    def get_scores(self, query, docs, ltc):
        scores = {}
        for doc in docs:
            lnc = self.lnc_document(query, parse_abstract(get_doc_by_name(doc)))
            lnc_ltc = self.calculate_lnc_ltc(lnc, ltc)
            scores[doc] = round(lnc_ltc, 2)

        return scores

    """ Tale n elemets from an iterable list """
    def take(self, n, iterable):
        return list(islice(iterable, n))

    """ Search in ranked retrieval model """
    def search(self, query, K):
        query = query.split()
        words_query = lemmatize(query)
        if (self.idf == None):
            self.idf = self.create_idf()
        ltc = self.ltc_query(self.create_tf(words_query))
        docs = self.get_documents_of_query(words_query)
        scores = self.get_scores(words_query, docs, ltc)
        sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)
        top_K = self.take(K, sorted_scores)

        return top_K
