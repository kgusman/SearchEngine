# SearchEngine
Simple SearchEngine using NLTK, inverted index and ranked retrieval model. Corpus based on documents from open [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/index.php).

Dataset - [NSF Research Award Abstracts 1990-2003 Data Set ](http://archive.ics.uci.edu/ml/datasets/NSF+Research+Award+Abstracts+1990-2003) - consists 112 000 documents with necessary information about articles including abstracts.
In my case, I search information from this abstracts.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- [NLTK](http://www.nltk.org/) installed
- [Python 3](https://www.python.org/downloads/) installed

### Installing
Download this repository and execute **main.py** file.
```angular2html
git clone https://github.com/camilldesmoulins/SearchEngine
cd SearchEngine/
python3 main.py
```

## Architecture
The whole system built using Python 3 language, because this language has a huge functionality and very handy for this kind of tasks.
Project files divided by their purposes.
- *engine.py* is a command-based interface for making dialogs with a user.
- *invInd.py* consists necessary functions for working with a corpus and creating an inverted index.
- *search.py* consists functions for searching document by his id and process queries for searching.
- *rankedRet.py* consists functions for ranked retrieval search model.

For convenience, corpus divided to three parts, which can be chosen in inverted index and ranked retrieval settings:
- Documents from 1990s. Size of a part: 10093
- Documents from 1990-1994. Size of a part: 51663
- Documents from 1990-2003. Size of a part: 132038

By default, the engine creates the inverted index for the first part. An average time of creating the index for this part - 300 seconds.
And for ranked retrieval model engine uses documents from small folder of the first part, which consists 379 documents.

## Screenshots
![Alt text](./Screenshots/Helper.png?raw=true "Help command")
![Alt text](./Screenshots/queryEx.png?raw=true "Example of a query")
![Alt text](./Screenshots/getDoc.png?raw=true "Example of a doc")
![Alt text](./Screenshots/rankedret.png?raw=true "Example of a ranked retrieval model search")

## Authors
**Kamill Gusmanov** - [camilldesmoulins](https://github.com/camilldesmoulins)

## License
This project is licensed under the MIT License.
