from invInd import create_inverted_index


def print_help():
    pass

if __name__ == "__main__":
    inverted_index = None
    command = ""
    print("Welcome to SearchEngine! Type '\h' for help.")
    while True:
        response = input("Enter command: ")
        if response == "\h":
            print_help()
        if response == "\q":
            break

    print("Quitting...\nBye!")
