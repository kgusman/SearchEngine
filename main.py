from invInd import create_inverted_index

class CommandLine():
    def __init__(self):
        self.inverted_index = None

    def print_help(self):
        pass

    def execute_search(self):
        print("Please, use boolean query type for serchin in corpus.\nExample: 'dogma & population'\nFor more \\"
              "examples within github repo.")
        query = input("Enter query: ")
        pass

    def change_index(self):
        pass

    def create_index(self):
        if self.inverted_index == None:
            inverted_index = create_inverted_index()

    def get_document(self):
        id = input("Enter the document name: ")
        pass


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
                print("Wring command. Type '\h' for help.")

        print("Quitting...\nBye!")

if __name__ == "__main__":
    app = CommandLine()
    app.dialog()
