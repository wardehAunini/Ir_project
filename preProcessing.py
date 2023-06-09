import re
from nltk import word_tokenize, edit_distance
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
correct_words = words.words()
stopwordslist = stopwords.words("english")
stopwordslist.append("NaN")
lemmatizer = WordNetLemmatizer()
regex = re.compile(r"\d{1,7}_\d{1,2}");

regexBWT = re.compile(r"^\.[BWTNA]$")

regexA = re.compile(r"^\.[A]$")
regexX = re.compile(r"^\.X")
regexW = re.compile(r"^\.W")
year = re.compile(r"^[12]\d\d\d$")
numb = re.compile(r"\d")

def add(dictionary, word, docs):
    cnt = 0
    if word not in dictionary:
        for doc in docs:
            found = False
            if word in doc.split():
                found = True
            if found:
                cnt += 1
        dictionary[word] = cnt


# table de traduction pour enlever les car. spéciaux, remplace les '-' par des espaces
table = str.maketrans('-()', '   ',"!\"#$%&'*+./:;<=>?@[\]^_`{|}~,")  # table de traduction pour enlever les car. spéciaux


def removeSpecialChar(line):
    new_line = ''
    for word in line:
        new_line += (word.translate(table))
    return new_line



def removeCommonWords(text):
    string = ''
    if text not in stopwordslist:
        string += text + ' '
    return string


def processingText(filename):
    print("processing "+filename+"...")

    output = open('Generated_files/' + filename + '_processing', 'w')
    input = open('Data_files/'+filename, 'r')

    text = input.readlines()
    porter = PorterStemmer()
#    lemmatizer = WordNetLemmatizer()

    isAuthor = False
    isX = False
    for line in text:
        if re.search(regex,line):
            isX = False
            isAuthor=False

        if re.search(regexBWT,line):

            isX=False
        if re.search(regexX, line):
            isX = True


        if not ((re.search(regex, line)) or (re.search(regexBWT,line))):
            if isAuthor:
                output.write("")
            if isX:
                 output.write("")

            else:

                newline = removeSpecialChar(line)
                newline = newline.lower()
                newline = removeCommonWords(newline)
                for word in newline.split():
                    stemmed = porter.stem(word)
                    lemmatized = lemmatizer.lemmatize(stemmed)
                    output.write(lemmatized +" ")



                output.write('\n')
        else:
            output.write(line)
    return("processing done")


def generateDict(filename):
    print("Generating dict for "+filename+"...")
    dico = dict()

    separator = ' '
    lexi = open('Generated_files/'+filename+'_dictionary', 'w')
    processingText(filename)
    data = open('Generated_files/'+filename + '_processing').readlines()

    docs = []
    doc = []

    for line in data:
        if re.search(regex, line):
            string = separator.join(doc)
            docs.append(string)
            doc = []
        else:
            doc.append(line)
    docs.append(separator.join(doc))
    docs.pop(0)

    for doc in docs:
        for word in doc.split():
            if re.search(numb, word):
                if re.search(year, word):
                    add(dico, word, docs)
            else:
                add(dico, word, docs)

    for w in sorted(dico):
        if dico[w]:
            lexi.write(w + "," + str(dico[w]) + "\n")  # version avec la fréquence
    print("dictionary done")

    return("pre processing done")



def writeQuery(filename,query):
    output = open('Data_files/' + filename, 'w')
    output.write(query)
    return ("done")

