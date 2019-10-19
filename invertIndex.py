from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import rocksdb
import os
os.system('rm test.db/LOCK')

sc =SparkContext()

# rdd = sc.wholeTextFiles("hdfs://localhost:9000/Users/omarkhursheed/mini-google/Project1_data/Project1_data")
# idurlmap = sc.wholeTextFiles("hdfs://localhost:9000/Users/omarkhursheed/mini-google/idUrlMap")
rdd = sc.wholeTextFiles("hdfs://localhost:9000/hddata/Project1_data/")
idurlmap = sc.wholeTextFiles("hdfs://localhost:9000/hddata/idUrlMap")

urlmap = idurlmap.map(lambda x: x[1].split('\n'))
flats = urlmap.flatMap(lambda x:[(lin, lin.split(',')[0]) for lin in x] )
flatsUp = flats.map(lambda x: (x[1], x[0]))
flatsDown = flatsUp.map(lambda x: (x[0], x[1].split(',')[1]))


#Changing the keys to contain only of the format 'doc_0'
forward_map = rdd.map(lambda x : (x[0].split('/')[-1].split('.')[0], x[1]))
#Splitting the dictionary into several key value pairs of the form ('doc_0', 'amherst')
splitForwardMap = forward_map.flatMap(lambda x:[(x[0], word) for word in x[1].lower().replace(',','').replace('.','').replace('?','').split()])
#keeping only the unique key-value pairs be removing the duplicates as we don't need to store the count for now.
splitForwardMap = splitForwardMap.distinct()


#Creating inverted index from the existing ones
inverted_map = splitForwardMap.map(lambda x: (x[1], [x[0]])).reduceByKey(lambda a,b: a+b)

db = rocksdb.DB("test-1.db",rocksdb.Options(create_if_missing=True))
for c in inverted_map.collect():
	print(c[0],c[1])
	db.put(c[0].encode(),str(c[1]).encode())	
#Some experiments with read write of RDDs
#These are not needed in the future once we implement rocksdb
# inverted_map.saveAsTextFile("hdfs://localhost:9000/hddata/results/test4")
# newRdd = sc.textFile("hdfs://localhost:9000/hddata/results/test4").map(lambda x : [(str, list)])
# print(newRdd.take(1))

#Example function for pvta
#Getting the docids for pvta
"""
query = input("Enter the query you want to search for:\n")

words = query.replace(',','').replace('.','').replace('?','').split()

results = []

print(words)
for word in words:
    newresults = inverted_map.filter(lambda x: word.lower() in x[0]).collect()
    if len(newresults) > 0:
        results += newresults[0][1]

results = list(dict.fromkeys(results))

print(len(results))

if len(results) >0:
    #Getting the corresponding urls for the docIds
    docIdToUrls = flatsDown.filter(lambda x: x[0] in results)
    listOfDocIdtoUrls = docIdToUrls.take(len(results))
    for docIdToUrl in listOfDocIdtoUrls:
        print(docIdToUrl)
else:
    print('No results match your query. Please try something else !!')


# print(umas.take(1))
"""