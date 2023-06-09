
import os
from collections import OrderedDict
import math
import json

RELEVANCEJUDGEMENT_FILE_PATH = 'Data_files/qrels.txt'
RETRIEVAL_MODELS_PATH = 'Generated_files/result.res'
EVALUATION_RESULTS_FILE_PATH = 'Generated_files/EvaluationResults.txt'
SUMMARY_FILE_NAME = 'Generated_files/summary.txt'

relevanceJudgements = {}

def retrieveRelevanceJudgement():
    with open(RELEVANCEJUDGEMENT_FILE_PATH, 'r') as f:
        for relevanceJudgement in f:

            items = relevanceJudgement.split(' ')

            queryID = items[0]
            documentID = items[1]

            # add into relevance judgement dictionary
            if queryID in relevanceJudgements:
                relevanceJudgements[queryID].append(documentID)
            else:
                relevanceJudgements[queryID] = [ documentID ]
    f.close()

def retrieveQueryResults(fileName):
    queryResults = OrderedDict()
    with open(fileName, 'r') as fr:
        for queryResult in fr:
            items = queryResult.split('		')
            queryID = items[0]
            documentID = items[1]
            if queryID in queryResults:
                queryResults[queryID].append(documentID)
            else:
                queryResults[queryID] = [ documentID ]
    fr.close()
    return queryResults

def calculateMeasure(fileName, queryResults, summary):
    AP = []
    RR = []
    P5 = []
    P10 = []
    fw = open(fileName, 'w')
    fw1 = open(summary, 'w')
    for queryID in queryResults:
        psum = 0
        rr = 0
        results = queryResults[queryID]
        rank = 0
        relevantNumber = 0
        relevantDocuments = []
        # exclude queries which don't have relevant documents
        if queryID in relevanceJudgements:
            relevantDocuments = relevanceJudgements[queryID]

        else:
            continue
        for document in results:
            rank += 1
            isRelevant = 0
            if document in relevantDocuments:

                if relevantNumber == 0:
                    rr = 1 / (rank * 1.0)
                relevantNumber += 1
                isRelevant = 1
            precision = relevantNumber / (rank * 1.0)
            # AP
            if isRelevant == 1:
                psum += precision
            # P@5
            if rank == 5:
                P5.append(precision)
            # P@10
            if rank == 10:
                P10.append(precision)
            recall = 0 if len(relevantDocuments) == 0 else relevantNumber / (len(relevantDocuments) * 1.0)

        fw.write( 'queryID : '+queryID + ' '  +'precision : ' + str("{:.3f}".format(precision)) + ' ' +'recall : '+  str("{:.3f}".format(recall)) + '\n')
        if relevantNumber != 0:
            AP.append(psum / (relevantNumber * 1.0))
        else:
            AP.append(0.0)
        RR.append(rr)

    fw1.write('MAP = ' + str("{:.3f}".format(math.fsum(AP) / len(AP))) + '\n')
    fw1.write('MRR = ' + str("{:.3f}".format(math.fsum(RR) / len(RR))) + '\n')
    fw1.write('Mean P@5 = ' + str("{:.3f}".format(math.fsum(P5) / len(P5))) + '\n')
    fw1.write('Mean P@10 = ' + str("{:.3f}".format(math.fsum(P10) / len(P10))) + '\n')
    fw1.close()
    fw.close()
    array = [{'key': '1', 'MAP': str("{:.3f}".format(math.fsum(AP) / len(AP))) , 'MRR': str("{:.3f}".format(math.fsum(RR) / len(RR))) ,'P@10':str("{:.3f}".format(math.fsum(P10) / len(P10))) } ]
    return array

def evaluation(path):
    with open(EVALUATION_RESULTS_FILE_PATH + SUMMARY_FILE_NAME, 'w') as summary:
        for fileName in os.listdir(path):
            if fileName == '.DS_Store':
                continue

            runName = fileName[0:fileName.find('.txt')]
            summary.write(runName + '\n')

            # read query results from previous file
            queryResults = retrieveQueryResults(path + fileName)
            # calculate measure
            calculateMeasure(EVALUATION_RESULTS_FILE_PATH + 'evaluation_' + fileName, queryResults, summary)

    summary.close()

def  mainEva():
    retrieveRelevanceJudgement()
    queryResults = retrieveQueryResults(RETRIEVAL_MODELS_PATH)
    summaryEva=calculateMeasure(EVALUATION_RESULTS_FILE_PATH , queryResults, SUMMARY_FILE_NAME)
    return json.dumps(summaryEva)
def evaResult():

 with open('Generated_files/EvaluationResults.txt', 'r') as fr:
     prescion=[]
     recall=[]
     id = []

     for queryResult in fr:
         items = queryResult.split(' ')
         prescion.append(items[5])
         recall.append(items[8])
         id.append(items[2])
     array = [{'key': id[i], 'prescion': prescion[i],'recall':recall[i]} for i in range(len(prescion))]
     return json.dumps(array)


