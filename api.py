
from __future__ import division
import sys
import re
from flask import Flask, app, request
from preProcessing import *
from indexing import *
from research_engine import *
from evaluation import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/ProcessingDataFile', methods=[ 'POST'])
def processingDataFile():
       return generateDict(request.form['filename'])
@app.route('/ProcessingQueryFile', methods=['POST'])
def processingQueryFile():
       return generateDict(request.form['filename'])
@app.route('/WriteQuery', methods=['POST'])
def WriteQuery():
       return writeQuery(request.form['filename'],request.form['query'])
@app.route('/IndexingDOC', methods=['POST'])
def IndexingDOCS():
       docs = "Generated_files/"+request.form['filename']+"_processing"
       return main_indexing(docs, "DOCS",request.form['filename'])
@app.route('/IndexingQRYS', methods=['POST'])
def IndexingQRY():
       queries = "Generated_files/"+request.form['filename']+"_processing"
       return main_indexing(queries, "QRYS",request.form['filename'])
@app.route('/Matching', methods=['POST'])
def reserch():
       return mainReserch()
@app.route('/Result', methods=['POST'])
def re1():
       return returnk(request.form['query'],request.form['filename'])

@app.route('/EVALUTION', methods=['POST'])
def EVALUTION():
       return mainEva()
@app.route('/EvaSummary', methods=['POST'])
def rr():
       return evaResult()
@app.route('/aa', methods=['POST'])
def ad():
       return aa()

app.run()

