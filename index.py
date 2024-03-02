# Indexer
# Create an inverted index for the corpus with data structures designed by you.
# • Tokens: all alphanumeric sequences in the dataset.

# Stop words: do not use stopping while indexing, i.e. use all words, even the frequently occurring ones.
# • Stemming: use stemming for better textual matches. Suggestion: Porter stemming, but it is up to you to choose.
# • Important text: text in bold (b, strong), in headings (h1, h2, h3), and in titles should be treated as more important than the in other places.
# Verify which are the relevant HTML tags to select the important words.

import math
import os
import re
import pandas as pd
from bs4 import BeautifulSoup as BS
import time
#import nltk
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer as PS
from collections import defaultdict
import json
import pandas


#dev = "C:\Users\j_aja\PycharmProjects\CS121projects\Assignment3\DEV"
#dev = "C:\Users\j_aja\PycharmProjects\CS121projects\Assignment3\DEV"
#dev = "C:\Test\DEV" # os.path.join(os.getcwd(), "DEV")
dev = os.path.join(os.getcwd(), "DEV")

dev = "./DEV/"

doc_id_dict = dict()
term_id_dict = dict()
term_n_doc_dict = dict()
count_words = 0
doc_id = 0
def bool_num(word) -> bool:
    return word.isdigit()
def save():
    global doc_id_dict
    global term_id_dict
    global term_n_doc_dict
    global count_words
    global doc_id

    saved_files = 0
    Dir_files = len(os.listdir(dev))
    doc_id = ''
    doc_num = 0
    for directory in os.listdir(dev):

        for fn in os.listdir(dev + directory):
            try:
                #print("dirs: ", dev, " subdirs: ", directory, " files: ", fn)
                with open(dev + './' + directory + '/' + fn) as data_file:
                    j_data = json.load(data_file)
                    #print(j_data)
                    doc_id = fn
                    doc_num += 1
                    doc_url = j_data["url"]
                    doc_id_dict[doc_id] = doc_url
                    pagewords = j_data["content"].split()
                    for term in pagewords:
                        encoded_term = term.encode('utf8')
                        if(not bool_num(encoded_term)):
                            value = term_id_dict.get(encoded_term)

def index(doc_id, current_id, alpha_sequences, first_rank, second_rank):

    if doc_id % 11000 == 0:
        write()

    word_freq = defaultdict()

    for word in alpha_sequences:
        word_freq[word] += 1

    for word in alpha_sequences:
        score = round(word_freq[word] / len(alpha_sequences), 7)

    for word in alpha_sequences:
        try:
            if first_rank[word]:
                score += 1
            if second_rank[word]:
                score += 0.5
        except:
            pass

        finally:
            if word not in inverse_index:
                first_time = (current_id, score)
                inverse_index[word] = set()
                inverse_index[word].add(first_time)
            else:
                inverse_index[word].add((current_id, score))
    word_freq.clear()

def write():
    global index_count
    global unique_words
    global total_indoc
    global doc_id
    global current_id
    global inverse_index

    index_count += len(inverse_index)
    total_indoc += doc_id
    index_count += 1
    doc_id = 0
    save_path = os.path.join(os.getcwd(), "Test")

    sent_text = open(os.path.join(save_path, f"info{index_count}" + ".txt"), 'w')
    extra_text = open(os.path.join(save_path, f"info_urls{index_count}" + ".txt"), 'w')

    with sent_text as json_file:
        inverse_index = {k: str(v) for k, v in sorted(inverse_index.items())}
        json.dump(inverse_index, json_file)
    sent_text.close()

    with extra_text as index_json_file:
        doc_id = {k: v for k, v in sorted(doc_id.items())}
        json.dump(doc_id, index_json_file)
    extra_text.close()

    inverse_index.clear()
    doc_id.clear()

def tokenize(content):
    """
    Runtime Complexity: O(n)
    """
    tList = []
    token_word = ""
    content = content.split()
    ps = PS()

    for w in content:
        token_word = re.sub("[^A-Za-z0-9]+", " ", str(w))
        token_word = re.sub("_", " ", str(token_word))
        token_word = token_word.strip()

        if len(token_word.split()) > 1:
            for token in token_word.split():
                stem_token = ps.stem(token)
                if len(stem_token) >= 2:
                    tList.append(stem_token)
    return tList

def calculate(txtfile):
    final_index = {}
    with open(txtfile, "r") as file:
        text_response = json.loads(file.read())

        for word, posting in text_response['all_pages'].items():
            posts = re.sub('}', '}, ', str(posting))
            posts = eval(posts)[0]
            new_postings = list()

            for (docID, score) in posts:
                idf = math.log(270526 / len(posts) + 1)
                new_postings.append((docID, round(score * idf, 7)))
            final_index[word] = new_postings

    save_path = os.path.join(os.getcwd(), "Test")
    score_dict = open(os.path.join(save_path, "score_dict.txt"), 'w')
    with score_dict as file:
        file.write(json.dumps(final_index))
    score_dict.close()

def main(dev):
    global doc_id
    global current_id

    for subdir, dirs, files in os.walk(dev): # iterates through DEV
        for file in files:
            datafile = os.path.join(subdir, file)
            doc_id += 1
            current_id += 1
            alpha_sequences = list()
            print(f"File: DOCUMENT ID:{doc_id} INDEX COUNT:{index_count} WORDS:{unique_words} CURRENT ID:{current_id}: ", datafile)

            first_rank = dict()
            second_rank = dict()

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

        doc_dict[current_id] = datafile[49:]

    except Exception as error:
        print("There is an error at: " + str(error))

    partial_index()
    save_path = os.path.join(os.getcwd(), "Test")
    final_text = os.path.join(save_path, "final_text.txt")
    calculate(final_text, total_indoc)


def partial_index():
    global index_count
    global unique_words
    global total_indoc
    global doc_id
    global current_id
    global inverse_index
    global doc_dict

    unique_words += len(inverse_index)
    index_count += 1
    total_indoc += doc_id

    save_path = os.path.join(os.getcwd(), "Test")

    info = os.path.join(save_path, f"info{index_count}" + ".txt")
    info_urls = os.path.join(save_path, f"info_urls{index_count}" + ".txt")

    sent_text = open(info, 'w')
    extra_text = open(info_urls, 'w')

    with sent_text as json_file:
        inverse_index = {k: str(v) for k, v in sorted(inverse_index.items())}
        json.dump(inverse_index, json_file)
    sent_text.close()

    with extra_text as index_json_file:
        doc_dict = {k: v for k, v in sorted(doc_dict.items())}
        json.dump(doc_dict, index_json_file)
    extra_text.close()

    file_list = [os.path.join(save_path, f"info{x + 1}" + ".txt") for x in range(index_count)]
    url_list = [os.path.join(save_path, f"info_urls{x + 1}" + ".txt") for x in range(index_count)]

    base = []
    for file in file_list:
        temp = pandas.read_json(file, orient = "index")
        base.append(temp)

    result = base[0]
    result.columns = ["pages1"]
    count = 2
    for i in base[1:]:
        i.columns = [f'pages{count}']
        count += 1
        result = result.join(i, how = "outer", lsuffix = "_left", rsuffix = "_right")

    result = result.fillna('')
    result['all_pages'] = result['all_pages'] = result["pages1"] + result["pages2"] + result[
        "pages3"] + result["pages4"] + result["pages5"] + result["pages6"]
    for i in range(index_count):
        del result[f'pages{i + 1}']

    total_urls = []
    for urls in url_list:
        temps = pandas.read_json(urls, orient = 'index')
        total_urls.append(temps)
    url_result = pandas.concat(total_urls)
    save_path = os.path.join(os.getcwd(), "Test")

    final_text = os.path.join(save_path, "final_text.txt")
    final_url = os.path.join(save_path, "final_url.txt")

    result.to_json(final_text)
    url_result.to_json(final_url)

if __name__ == "__main__":
    start = time.time()
    print("DEV: ", dev)
    main(dev)
    print("\nResults: ")
    print("--- %s seconds ---" % (time.time() - start))
    # Number of indexed document?
    print("Number of indexed document: " + str(total_indoc) + " " + str(current_id))
    # Number of unique words?
    print("Number of unique words: " + str(unique_words))
    # Total size of index on disk?
    print("Total size of index on disk: ", pd.Index)
