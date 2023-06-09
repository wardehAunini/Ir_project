import re
import time
from tools import *
import sys
import django
from django.urls import reverse
import collections
freqInf = 0
freqSup = 1400

def reverse_double_dict(dico):
    flipped = collections.defaultdict(dict)
    for key, val in dico.items():
        for subkey, subval in val.items():
            flipped[subkey][key] = subval

    return flipped


def readDictionary(pathLexique):
    dictionary_file = open(pathLexique)
    dicti = dictionary_file.read().splitlines() 
    dictionary = {}
    for line in dicti:
        line = line.split(",")
        while '' in line :
            line.remove('')
        if freqInf < float(line[1]) < freqSup:
            dictionary[line[0]] = float(line[1])
    dictionary_file.close()
    return dictionary



def extract_w_doc(words_doc, doc, nbDocs, title,dictionary):
    words_doc_occ = {}
    total_words = 0
    for ligne in doc:
        for word in ligne.split():
            total_words += 1
            if word in dictionary:
                if word not in words_doc_occ:
                    words_doc_occ[word] = 1
                else:
                    words_doc_occ[word] += 1


    for word in title.split():
        total_words += 1
        if word in dictionary:
            if word not in words_doc_occ:
                words_doc_occ[word] = 1
            else:
                words_doc_occ[word] += 1


    for word in words_doc_occ:
        freqWord = words_doc_occ[word] / total_words
        TF = freqWord

        IDF = nbDocs / dictionary[word]

        words_doc[word] = str((TF) * (IDF))


    for word in title.split():
        if word in words_doc_occ:
            words_doc[word] = str(float(words_doc[word]))


def write_dict(fichier, dico):
    for elem in dico:
        fichier.write(elem)
        for obj in dico[elem]:
            fichier.write("," + obj + "," + dico[elem][obj])
        fichier.write("\n")


def main_indexing(path, extension,filename):
    dictionary = readDictionary("Generated_files/" + filename
    +"_dictionary")
    regex = re.compile(r"\.I\s(\d+)\s$")
    regexTitle = re.compile(r"^\.T$")
    regexW = re.compile(r"^\.[W]$")
    data = open(path)

    index = {}
    docs = {}
    text_doc = ""
    num_doc = -1  # -1
    dic_titles = {}
    is_title = -1

    title = ""


    for line in data:
        match = re.search(regex, line)
        if match:
            num_doc = match.group(1)
            mots_doc = {}
            index[num_doc] = mots_doc
            text_doc = []
            docs[num_doc] = text_doc

            is_title = -1
            dic_titles[
                num_doc] = ""
        elif re.search(regexTitle, line):
            is_title = 1

        elif is_title == 1:
            if re.search(regexW, line):
                is_title = -1

                dic_titles[num_doc] = title
                title = ""
            else:
                title += (line.rstrip('\n'))

        else:
            text_doc.append(line.rstrip('\n'))

    for num in docs:
        extract_w_doc(index[num], docs[num], len(docs), dic_titles[
            num],dictionary)

    data.close()


    reverse_index = reverse_double_dict(index)


    res = open("Generated_files/index." + extension, "w")
    write_dict(res, reverse_index)
    res.close()
    return ("done")


