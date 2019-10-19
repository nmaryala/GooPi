from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import flask
from flask import request, jsonify
import rocksdb
import os
os.system('rm test.db/LOCK')

app = flask.Flask(__name__)
app.config["DEBUG"] = True


sc =SparkContext()
idurlmap = sc.wholeTextFiles("hdfs://localhost:9000/hddata/idUrlMap")
#idurlmap = sc.wholeTextFiles("hdfs://localhost:9000/Users/omarkhursheed/mini-google/idUrlMap")

urlmap = idurlmap.map(lambda x: x[1].split('\n'))
flats = urlmap.flatMap(lambda x:[(lin, lin.split(',')[0]) for lin in x] )
flatsUp = flats.map(lambda x: (x[1], x[0]))
flatsDown = flatsUp.map(lambda x: (x[0], x[1].split(',')[1]))

@app.route('/', methods=['GET'])
def home():
    return '''<h1>GooPi Search</h1>
<p>Go to http://127.0.0.1:5000/api/v1/search/?query=diabetes and change the keyword after query in the URL to run for your own.</p>'''

@app.route('/api/v1/search/', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    query = None
    print(request.args)
    if 'query' in request.args:
        query = request.args['query']
    else:
        return "Error: No id or author field provided. Please specify an id."

   

    # query = input("Enter the query you want to search for:\n")

    words = query.replace(',','').replace('.','').replace('?','').split()

    db = rocksdb.DB("test-1.db",rocksdb.Options(create_if_missing=True))

    results = []

    for word in words:
        if(db.get(word.encode().lower()) is not None):
            newresults = (db.get(word.encode().lower())).decode()
            newresults = eval(newresults)
            if len(newresults) > 0:
                results.extend(newresults)
        results = list(set(results))    
    print(results)


    listOfDocIdtoUrls = []
    if len(results) >0:
        #Getting the corresponding urls for the docIds
        docIdToUrls = flatsDown.filter(lambda x: x[0] in results)
        listOfDocIdtoUrls = docIdToUrls.take(len(results))
        for docIdToUrl in listOfDocIdtoUrls:
            print(docIdToUrl)
    else:
        print('No results match your query. Please try something else !!')

    return jsonify(listOfDocIdtoUrls)


app.run()
# print(umas.take(1))
