from invInd import create_inverted_index
import sys
from search import *

class CommandLine():
    def __init__(self):
        self.inverted_index = None

    def print_help(self):
        f = open('help.txt')
        for line in f:
            sys.stdout.write(line)
        f.close()

    def execute_search(self):
        print("Please, use boolean query type for serchin in corpus.\nExample: 'dogma & population'\nFor more \\"
              "examples within github repo.")
        query = input("Enter query: ")
        pass

    def change_index(self):
        type = input("Enter type for an index (1, 2 or 3): ")
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

if __name__ == "__main__":
    app = CommandLine()
    app.dialog()
