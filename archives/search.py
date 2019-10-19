from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import rocksdb
import os
os.system('rm test.db/LOCK')


sc =SparkContext()
#idurlmap = sc.wholeTextFiles("hdfs://localhost:9000/hddata/idUrlMap")
idurlmap = sc.wholeTextFiles("hdfs://localhost:9000/Users/omarkhursheed/mini-google/idUrlMap")

urlmap = idurlmap.map(lambda x: x[1].split('\n'))
flats = urlmap.flatMap(lambda x:[(lin, lin.split(',')[0]) for lin in x] )
flatsUp = flats.map(lambda x: (x[1], x[0]))
flatsDown = flatsUp.map(lambda x: (x[0], x[1].split(',')[1]))



query = input("Enter the query you want to search for:\n")

words = query.replace(',','').replace('.','').replace('?','').split()

db = rocksdb.DB("test-1.db",rocksdb.Options(create_if_missing=True))

results = []

for word in words:
    newresults = (db.get(word.encode())).decode()
    newresults = eval(newresults)
    if len(newresults) > 0:
        results.extend(newresults)
results = list(set(results))    
print(results)



if len(results) >0:
    #Getting the corresponding urls for the docIds
    docIdToUrls = flatsDown.filter(lambda x: x[0] in results)
    print(docIdToUrls)
    listOfDocIdtoUrls = docIdToUrls.take(len(results))
    for docIdToUrl in listOfDocIdtoUrls:
        print(docIdToUrl)
else:
    print('No results match your query. Please try something else !!')

#now rdd holds the inverted map again

