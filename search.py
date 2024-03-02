# Searcher

#   search and retrieval component
#   At least the following queries should be used to test your retrieval:
#   cristina lopes, machine learning, ACM, master of software engineering

DOC_IDS_FILE = "./docsIDs.txt"
INV_INDEX_FILE = "./InvIndex_dict.txt"
TERMS_IDS_FILE = "./termsIDs.txt"
DEV_FILE = "./ANALYST/"

def search(text):
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

def scabTermID():
    term_ID_dict = dict()

    with open(TERMS_IDS_FILE, "r") as termfile:
        lines = set(termfile.readlines()[1:])
        for line in lines:
            data = line.split(" ")
            termId = data[0].strip()
            term = data[1].strip()

            term_ID_dict[term] = termId

    return term_ID_dict
def scanContent():
    
def scanURL():
    
def scanID():
    

def wordfrequency():
    
def FindALL():
    
    
def calculateALL():
    
    

def main():
    input = search("Enter input: ").strip().lower()
    while input != "":
        input = search("Enter query: ").strip()

if __name__ == "__main__":
    main()