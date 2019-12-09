#### COMPSCI532_Project1

# **Introduction**: Project GooPi - The ultimate Search Engine


#### Features:
1. Crawled webpages are stored in hadoop file system (HDFS) 
2. Forward and reverse indices are created by using Apache Spark
3. PySpark is used rather than Scala as the programming language.
4. Inverted index is stored in RocksDB, an extremely fast database management system with great response time.
5. Can take multiple word inputs for search and combine results in an intutive way.
6. Can get results for part of the query if no results are obtained for that query.

#### Text Processing Techniques:
1. Removing ',' '.' from the words while creating indices
2. Converting all the words to lower case before indexing
3. Splitting words while searching for multi-word phrases.
4. Removing ',' '.' '?' while searching as well from the phrase and converting them to lower case.

#### Instructions to Run:
Please follow the below steps to make the search engine work in your machine.

Pre-requisites:
1. Make sure hadoop in installed and you should see namenode and datanode when you enter 'jps' command.
2. Make sure spark is installed. 
3. Python-rocksdb should be installed.
4. Flask in python should be installed. To install, do this: pip install flask

Pre-run instructions:
1. Go to your Hadoop folder and run the following commands.
   a). bin/hadoop namenode -format
   b). bin/hadoop datanode -format
2. Go to  localhost:50070/dfshealth.html and check NameNode interface.
3. Go to  localhost:50075/ to see if your datanode is up.
4. For any issues: Follow this tutorial: https://www.edureka.co/blog/install-hadoop-single-node-hadoop-cluster


Running instructions:
1. First pull the code to your local machine and go to the folder mini-google-group-8
2. Run 'bash putdata.sh'. Please give permissions with 'chmod +x putdata.sh' before running. This will do steps 3-5 for you.
3. This script first creates directories for and loads the data into your hdfs. 
4. Then it will create the reverse index by calling the invertIndex.py script andd load the data into rocksdb.
5. It will finally call search_api_new.py, and create the URL below for you to query. 
6. Go to the URL 'http://127.0.0.1:5000/api/v1/search/?query=diabetes'.
    a). Replace the word 'diabetes' with the query of your choice. Query could be of multiple words too. On Chrome, you may just add a space, for safari '%20' between words.
    b). Press Enter to see the results.
7. If you close the session and wish to create other queries without reloading data to hdfs and recreating the entire database, please call 'python search_api_new.py', and go to the URL above. If you get an Address already in use error, please close and restart your terminal window (This problem is so far found to be macOS specific).   

### Versions:
1. Spark - 2.4.4
2. Hadoop - Tested on 2.7.3 and 3.2.1
3. Python 3.7.3
4. Python-rocksdb - 0.7.0
5. Scala - 2.11.12
6. Java - Java 1.8.0_221

### Files
1. putdata.sh - A simple bash script to load data
2. invert_index.py - We create the inverted index and store it into rocksdb
3. search_api_new.py - File that handles HTTP requests and performs the search engine functionality

