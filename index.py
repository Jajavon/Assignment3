# Indexer
# Create an inverted index for the corpus with data structures designed by you.
# • Tokens: all alphanumeric sequences in the dataset.

# Stop words: do not use stopping while indexing, i.e. use all words, even the frequently occurring ones.
# • Stemming: use stemming for better textual matches. Suggestion: Porter stemming, but it is up to you to choose.
# • Important text: text in bold (b, strong), in headings (h1, h2, h3), and in titles should be treated as more important than the in other places.
# Verify which are the relevant HTML tags to select the important words.

import os
from bs4 import BeautifulSoup
import time

dev = "C:\Users\j_aja\PycharmProjects\CS121projects\Assignment3\DEV"
inverse_index = dict()
index_count = 0
unique_words = 0
total_indoc = 0
doc_id = 0
current_id = 0


def index(doc_id, current_id, alpha_sequences, first_rank, second_rank):

    if doc_id % 11000 == 0:
        write()

def index(pages):

def write():
    {}
def tokenize(text):
    """
    Runtime Complexity: O(n)
    """
    tList = []
    word = ""
    text = text.split()

    for i in range(len(text)):
        if (text[i].isalnum()):
            word += text[i].lower()
        else:
            if (len(word)) >= 3:
                tList.append(word)
                word = ""
            else:
                word = ""

    for w in tList:
       if w in rec.all:
           rec.all[w] += 1
       else:
           rec.all[w] = 1

def main():
    global doc_id
    global current_id

    first_rank = dict()
    second_rank = dict()
    for subdir, dirs, files in os.walk(dev): # iterates through DEV
        for file in files:
            datafile = os.path.join(subdir, file)
            doc_id += 1
            current_id += 1
            alpha_sequences = list()

    try:
        soup = BS(open(datafile), "html.parser")
        for content in soup.findAll(["title", "p", "b", re.compile('^h[1-6]$')]):
            data = content.getText().strip()
            alpha_sequences = word_tokenize(data)

        for content in soup.findAll(["title", re.compile('^h[1-3]$')]):
            data = content.getText().strip()
            first_rank = {**first_rank, **(Counter(word_tokenize(data)))}

        for content in soup.findAll(["b", "strong", re.compile('^h[1-3]$')]):
            data = content.getText().strip()
            second_rank = {**second_rank, **(Counter(word_tokenize(data)))}

        index(doc_id, current_id, alpha_sequences, first_rank, second_rank)

    except Exception as error:
        print("There is an error at: " + str(error))
        raise



if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("seconds:", end)