from tools import *
import operator
from math import sqrt
from flask import jsonify
import sys
import django
from django.urls import reverse
import collections
import re
import json
regex = re.compile(r"\.I\s\d+\s$");
limit = 0.03
def reverse_double_dict(dico):
    flipped = collections.defaultdict(dict)
    for key, val in dico.items():
        for subkey, subval in val.items():
            flipped[subkey][key] = subval
    return flipped

def rewrite_dict(tab) :
    dico = dict()
    for string in tab:
        string_tab = string.split(",")
        word = string_tab[0]
        dico[word] = dict()

        for i in range(1,len(string_tab),2):
            dico[word][int(string_tab[i])] = float(string_tab[i+1])

    return dico




def A(doc, qry) :
    result = 0
    for word in qry :
        if word in doc :
            result += qry[word] * doc[word]

    return result

def B(dico) :
    result = 0
    for word in dico :
        result += dico[word] * dico[word]
    return sqrt(result)







def mainReserch ():
    index_docs_file = open("Generated_files/index.DOCS")
    index_docs_tab = index_docs_file.read().splitlines()
    index_docs_file.close()

    index_qrys_file = open("Generated_files/index.QRYS")
    index_qrys_tab = index_qrys_file.read().splitlines()
    index_qrys_file.close()


    index_docs = reverse_double_dict( rewrite_dict(index_docs_tab) )
    index_qrys = reverse_double_dict( rewrite_dict(index_qrys_tab) )

    associations = dict()

    for qry,dic_qry in index_qrys.items() :
        associations[qry] =  {}
        for doc,dic_doc in index_docs.items() :
            score_doc = A(dic_doc, dic_qry) / (B(dic_doc) * B(dic_qry))

            if (score_doc > limit) :
                associations[qry][doc] = score_doc

    fichier = open("Generated_files/result.res","w")


    for qry in sorted(associations) :
        for doc in sorted(associations[qry]) :
            fichier.write(str(qry).zfill(2) + "		" + str(doc) + "		" + str(associations[qry][doc]) + "\n")

    fichier.close()
    return "done"

def returnk(query1,datafile):
    a=[]
    print("hi")

    dico = dict()
    index_docs_file = open("Generated_files/index.DOCS")
    index_docs_tab = index_docs_file.read().splitlines()
    index_docs_file.close()

    index_qrys_file = open("Generated_files/index.QRYS")
    index_qrys_tab = index_qrys_file.read().splitlines()
    index_qrys_file.close()


    index_docs = reverse_double_dict(
        rewrite_dict(index_docs_tab))
    index_qrys = reverse_double_dict(
        rewrite_dict(index_qrys_tab))
    associations = dict()

    for qry, dic_qry in index_qrys.items():
        associations[qry] = {}
        for doc, dic_doc in index_docs.items():

            score_doc = A(dic_doc, dic_qry) / (B(dic_doc) * B(dic_qry))

            if (score_doc > limit):
                associations[qry][doc] = score_doc


    for doc in sorted(associations[qry]):
        a.append(doc)

        separator = ' '
        data = open('Data_files/' + datafile ).readlines()

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
    for i in a :
        dico[i]=docs[i-1]
    array = [{'key': i, 'value': dico[i]} for i in dico]

    return json.dumps(array)











