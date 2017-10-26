from invInd import create_inverted_index
from search import *
from rankedRet import search
import sys
from configs import K

class CommandLine():
    def __init__(self):
        self.inverted_index = None

    def print_help(self):
        f = open('help.txt')
        for line in f:
            sys.stdout.write(line)
        f.close()

    def print_result(self, path):
        doc_list = path.split('/')
        print("Document: %s     Path: %s" %(doc_list[len(doc_list) - 1], path))

    def execute_search(self):
        type_of_search = input("Enter the type of a search: ")
        if type_of_search == "\inv":
            if self.inverted_index == None:
                print("Initialize inverted index...")
                self.create_index()
            print(
                "Please, use boolean query type for search in corpus.\nExample: 'dogma AND population'\nFor more examples use github repo.")
            query = input("Enter query: ")
            result = list(process_query(query, self.inverted_index))
            print("Number of results: %d" % (len(result[0])))
            for r in result[0]:
                self.print_result(r)
        elif type_of_search == "\\rank":
            print("Initialize ranked retrieval")
            query = input("Enter query: ")
            top = search(query, K)
            for elem in top:
                print("Document: %s -- score - %.2f" % (elem[0], elem[1]))
        else:
            print("Wrong type. Please try again.")


    def change_index(self):
        type = input("Enter type for an index (1, 2 or 3): ")
        print("Initialize inverted index...")
        if type == str(1):
            self.inverted_index = create_inverted_index()
        elif type == str(2):
            self.inverted_index = create_inverted_index(2)
        elif type == str(3):
            self.inverted_index = create_inverted_index(3)
        else:
            print("Wrong type of the index. Start again.")

    def create_index(self):
        if self.inverted_index == None:
            self.inverted_index = create_inverted_index()

    def get_document(self):
        id = input("Enter the document name: ")
        doc = get_doc_by_name(id)
        if doc == None:
            print("File not dound.")
        else:
            for line in doc:
                sys.stdout.write(line)
        print()
        doc.close()


    """
    '\h' - command for getting help
    '\q' - quit from the program
    '\s' - start searching in documents
    '\inv' - initialize search by inverted index
    '\rank' - initialize search by ranked retrieval
    '\i' - change number of documents for inverted index
    '\d' - get document by his name
    """
    def dialog(self):
        print("Welcome to SearchEngine! Type '\h' for help.")
        while True:
            response = input("Enter command: ")
            if response == "\h":
                self.print_help()
            elif response == "\q":
                break
            elif response == "\s":
                self.execute_search()
            elif response == "\i":
                self.change_index()
            elif response == "\d":
                self.get_document()
            else:
                print("Wrong command. Type '\h' for help.")

        print("Quitting...\nBye!")
