import sys

def search_docs(words, index):
    docs = []
    for word in words:
        docs.append(index[word])
    return docs

def get_doc_by_name(name):
    if name == None:
        return name
    ints = list(name)
    year = ints[0] + ints[1]
    month = ints[2] + ints[3]
    path = "./Corpus/"
    if int(year) >= 90 and int(year) <= 94:
        path += "Part 1/"
        path += "awards_19" + year + "/"
        path += "awd_19" + year + "_" + month + "/"
        path += "a" + name + ".txt"
    elif int(year) >= 95 and int(year) <= 99:
        path += "Part 2/"
        path += "awards_19" + year + "/"
        path += "awd_19" + year + "_" + month + "/"
        path += "a" + name + ".txt"
    elif year == '00' or year == '01' or year == '02' or year == '03':
        path += "Part 3/"
        path += "awards_20" + year + "/"
        path += "awd_20" + year + "_" + month + "/"
        path += "a" + name + ".txt"

    try:
        return open(path)
    except FileNotFoundError:
        return None
