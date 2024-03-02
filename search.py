# Searcher
import time
import os
import math
import json
import index
#   search and retrieval component
#   At least the following queries should be used to test your retrieval:
#   cristina lopes, machine learning, ACM, master of software engineering

DOC_IDS_FILE = "./docsIDs.txt"
INV_INDEX_FILE = "./InvIndex_dict.txt"
TERMS_IDS_FILE = "./termsIDs.txt"
DEV_FILE = "./ANALYST/"

def usersearch(text):
    return input(text)
def scanInvIndex():
    invIndex = dict()

    with open(INV_INDEX_FILE, "r") as indexFile:
        lines = set(indexFile.readlines())
        for l in lines:
            l= l.replace('\n', '')
            data = l.split(" ")
            doc_id = int(float(data[0].strip()))
            words = set(data[2:])
            invIndex[doc_id] = {}

            for w in words:
                t = w.strip()
                if t in invIndex[doc_id]:
                    invIndex[doc_id][t] += 1
                else:
                    invIndex[doc_id][t] = 1
    return invIndex;

def scanTermID():
    term_ID_dict = dict()

    with open(TERMS_IDS_FILE, "r") as termfile:
        lines = set(termfile.readlines()[1:])
        for line in lines:
            data = line.split(" ")
            termId = data[0].strip()
            term = data[1].strip()

            term_ID_dict[term] = termId

    return term_ID_dict
def scanContent(doc_id):
    json_dir = [dir for dir, subdir, json in os.walk(DEV_FILE) if doc_id in json][0]
    # print(json_dir)

    fn = os.path.join(json_dir, doc_id)
    text = ""
    try:
        with open(fn) as data:
            jsonData = json.load(data)
            content = str(jsonData["content"])
    except ValueError:
        print("No valid JSON in file: ", fn)
    # print("CONTENT: ", content)
    return content

def scanURL(doc_id):
    json_dir = [dir for dir, subdir, json in os.walk(DEV_FILE) if doc_id in json][0]

    fn = os.path.join(json_dir, doc_id)
    text = ""
    try:
        with open(fn) as data:
            jsonData = json.load(data)
            url_scanned = str(jsonData["url"])
    except ValueError:
        print("No valid JSON in file: ", fn)
    return url_scanned
def scanDocID():
    doc_id_dict = {}

    with open(DOC_IDS_FILE, "r") as docFile:
        lines = set(docFile.readlines()[1:])
        for l in lines:
            data = l.split(" ")
            doc_id = data[0].strip()
            doc = data[1].strip()

            doc_id_dict[doc_id] = doc

    return doc_id_dict

def wordfrequency(term, doc_id):
    words = scanContent(doc_id).lower().split()
    count = 0
    for word in words:
        if word == term:
            count += 1
        else:
            count = 1
    return 1 + math.log(int(count))

def FindALL(term_id, word, doc_id, doc_id_dict, index):
    pages = index[int(term_id)]
    if doc_id in pages:
        tf = wordfrequency(word, doc_id)
        idf = math.log(float(len(doc_id_dict)) / float(len(pages)))

        return float(tf * idf)
    else:
        return 0

def calculateALL(docs, term_id_dict, doc_id_dict, index, search, weight):
    cal_score = {}
    for doc in docs:
        for word in search:
            term_id = term_id_dict[word]
            found = FindALL(term_id, word, doc, doc_id_dict, index) * weight
            if doc not in cal_score:
                cal_score[doc] = found
            else:
                cal_score[doc] += found
    return cal_score

def saveSCORE(docs, term_id_dict, doc_id_dict, index, search, weight):
    score = dict()
    score.update(calculateALL(docs, term_id_dict, doc_id_dict, index, search, weight))
    return score
def BoolSearcher(word, term_id_dict, index):
    term_id = term_id_dict[word]
    pages = list(index[int(term_id)])
    return pages
def SearchTerm(searched, term_id_dict, doc_id_dict, index):
    Scores = {}

    valid_docs = set()
    good_docs = set()

    raw_search = set(searched.split())
    search = set()
    for word in raw_search:
        if word in term_id_dict:
            search.add(word)

    for word in search:
        checkDocs = BoolSearcher(word, term_id_dict, index)
        for doc in checkDocs:
            if doc not in valid_docs:
                valid_docs.add(doc)

    for doc in valid_docs:
        containsAll = True
        for word in search:
            termId = term_id_dict[word]
            valid_pages = index[int(termId)]
            if doc not in valid_pages:
                containsAll = False
                break

        if containsAll:
            good_docs.add(doc)
    for doc in good_docs:
        valid_docs.remove(doc)

    # print("valid Docs: ", valid_docs)
    # print("good Docs: ", good_docs)
    Scores.update(saveSCORE(good_docs, term_id_dict, doc_id_dict, index, search, 2.0))
    Scores.update(saveSCORE(valid_docs, term_id_dict, doc_id_dict, index, search, 1.0))
    return Scores

def printRESULTS(finalscores, doc_id_dict, searched):
    final_dict = ((k, finalscores[k]) for k in
              sorted(finalscores, key = finalscores.get, reverse = True)[:5])
    for key, value in final_dict:
        scannedURL = scanURL(key).strip()
        print("\nID: ", key, " ", doc_id_dict[key], "\n\tURL: ", scannedURL,
              "\n\tSearch: ", str(searched.split()))

def main():
    index = scanInvIndex()
    term_id_dict = scanTermID()
    doc_id_dict = scanDocID()
    input = usersearch("Enter input: ").strip().lower()

    while input != "":
        searchScores = SearchTerm(input, term_id_dict, doc_id_dict, index)
        printRESULTS(searchScores, doc_id_dict, input)
        input = usersearch("Enter query: ").strip()

if __name__ == "__main__":
    print("Starting")
    start = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start))
    print("Finished")