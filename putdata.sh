#Creating folders for putting data in hdfs
hdfs dfs -mkdir hdfs://localhost:9000/hddata
hdfs dfs -mkdir hdfs://localhost:9000/hddata/idUrlMap


#Putting data in hdfs
hdfs dfs -put    id_URL_pairs.txt   hdfs://localhost:9000/hddata/idUrlMap
hdfs dfs -put    Project1_data      hdfs://localhost:9000/hddata/


#Runnig pspark code to create inveted index and store it in rocksdb
python invertIndex.py

#Runnig Flask server code to server http queries
python search_api_new.py

