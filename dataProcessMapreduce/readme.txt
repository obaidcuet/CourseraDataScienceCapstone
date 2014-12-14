Note: if streaming show "failed with code 1" then issue with python code, like below:
PipeMapRed.waitOutputThreads(): subprocess failed with code 1

1. Create directories
# hadoop fs -mkdir /tmp/corpus/input
# hadoop fs -mkdir /tmp/corpus/ngrams
# hadoop fs -mkdir /tmp/corpus/indexedngrams
# hadoop fs -mkdir /tmp/corpus/finalindexedngrams

2. Copy files in HDFS:/tmp/corpus/input
# hadoop fs -ls /tmp/corpus/input
Found 3 items
-rw-r--r--   3 root supergroup  210160014 2014-12-12 11:54 /tmp/corpus/input/en_US.blogs.txt
-rw-r--r--   3 root supergroup  205811892 2014-12-12 11:54 /tmp/corpus/input/en_US.news.txt
-rw-r--r--   3 root supergroup  167105338 2014-12-12 11:54 /tmp/corpus/input/en_US.twitter.txt

3. make sure yran process have execurte permission on the python files, better change the group to hadoop and put 750 permission
cd /stage/AIU/corpus/
chmod 754 *.py
chown root:hadoop *.py

4. Create uniGrams:
4.1 Do below if not added in the profile:
export HADOOP_STREAMING=/opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar

4.2 Run mapreduce using haddoop streaming and python:
Note 1: in -mapper/-reducer only put the file names, put the full path in -files as comma seperated
Note 2: if any other files needed for lookup, also put the full path of that file in -files as comma seperated

4.3 Run mapreduce
hadoop fs -rm -r -skipTrash /tmp/corpus/ngrams/unigrams
hadoop jar $HADOOP_STREAMING -input /tmp/corpus/input/* -output /tmp/corpus/ngrams/unigrams  -file /stage/AIU/corpus/mapper_create_oneGrams.py -mapper mapper_create_oneGrams.py  -file /stage/AIU/corpus/reducer_create_nGrams.py -reducer reducer_create_nGrams.py -file /stage/AIU/corpus/profanity_words.txt 

4.4 Create an Imapala table with the unigram output location. Will be useful for sanity check.
impala-shell -i IP:PORT -d DBNAME
CREATE EXTERNAL TABLE UNIGRAMS
(
   NGRAMS STRING,
   FREQ INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/tmp/corpus/ngrams/unigrams';

INVALIDATE METADATA;

4.5 Do some checks
impala> select count(*) from UNIGRAMS;
impala> select count(distinct NGRAMS) from UNIGRAMS;

# hadoop fs -cat /tmp/corpus/ngrams/unigrams/*|wc -l

Above 3 command should have same output(in this case 998416)


5. create biGrams:
5.1  Do below if not added in the profile:
export HADOOP_STREAMING=/opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar

5.2 Run mapreduce
hadoop fs -rm -r -skipTrash /tmp/corpus/ngrams/bigrams
hadoop jar $HADOOP_STREAMING -input /tmp/corpus/input/* -output /tmp/corpus/ngrams/bigrams  -file /stage/AIU/corpus/mapper_create_twoGrams.py -mapper mapper_create_twoGrams.py  -file /stage/AIU/corpus/reducer_create_nGrams.py -reducer reducer_create_nGrams.py -file /stage/AIU/corpus/profanity_words.txt 

5.3 Create an Imapala table with the unigram output location. Will be useful for sanity check.
impala-shell -i IP:PORT -d DBNAME
CREATE EXTERNAL TABLE BIGRAMS
(
   NGRAMS STRING,
   FREQ INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/tmp/corpus/ngrams/bigrams';

INVALIDATE METADATA;

5.4 DO some checking
impala> select count(*) from BIGRAMS;
impala> select count(distinct NGRAMS) from BIGRAMS;

# hadoop fs -cat /tmp/corpus/ngrams/bigrams/*|wc -l

Above 3 command should have same output(in this case 13203263)
 

6. create trigrams:
6.1 Do below if not added in the profile:
export HADOOP_STREAMING=/opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar

6.2 Run mapreduce
hadoop fs -rm -r -skipTrash /tmp/corpus/ngrams/trigrams
hadoop jar $HADOOP_STREAMING -input /tmp/corpus/input/* -output /tmp/corpus/ngrams/trigrams  -file /stage/AIU/corpus/mapper_create_threeGrams.py -mapper mapper_create_threeGrams.py  -file /stage/AIU/corpus/reducer_create_nGrams.py -reducer reducer_create_nGrams.py -file /stage/AIU/corpus/profanity_words.txt 

6.3 Create an Imapala table with the unigram output location. Will be useful for sanity check.
impala-shell -i IP:PORT -d DBNAME
CREATE EXTERNAL TABLE TRIGRAMS
(
   NGRAMS STRING,
   FREQ INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/tmp/corpus/ngrams/trigrams';

INVALIDATE METADATA;

6.4 Checking
impala> select count(*) from TRIGRAMS;
impala> select count(distinct NGRAMS) from TRIGRAMS;

# hadoop fs -cat /tmp/corpus/ngrams/trigrams/*|wc -l

Above 3 command should have same output(in this case 35769259)


7. create quadGrams:
7.1 Do below if not added in the profile:
export HADOOP_STREAMING=/opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar

7.2 Run mapreduce
hadoop fs -rm -r -skipTrash /tmp/corpus/ngrams/quadgrams
hadoop jar $HADOOP_STREAMING -input /tmp/corpus/input/* -output /tmp/corpus/ngrams/quadgrams  -file /stage/AIU/corpus/mapper_create_fourGrams.py -mapper mapper_create_fourGrams.py  -file /stage/AIU/corpus/reducer_create_nGrams.py -reducer reducer_create_nGrams.py -file /stage/AIU/corpus/profanity_words.txt 

7.3 Create an Imapala table with the unigram output location. Will be useful for sanity check.
impala-shell -i IP:PORT -d DBNAME
CREATE EXTERNAL TABLE QUADGRAMS
(
   NGRAMS STRING,
   FREQ INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/tmp/corpus/ngrams/quadgrams';

INVALIDATE METADATA;

7.4 checking
impala> select count(*) from QUADGRAMS;
impala> select count(distinct NGRAMS) from QUADGRAMS;

# hadoop fs -cat /tmp/corpus/ngrams/quadgrams/*|wc -l

Above 3 command should have same output(in this case 49768190)



8. create pentaGrams:
8.1 Do below if not added in the profile:
export HADOOP_STREAMING=/opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar

8.2 Run mapreduce
hadoop fs -rm -r -skipTrash /tmp/corpus/ngrams/pentagrams
hadoop jar $HADOOP_STREAMING -input /tmp/corpus/input/* -output /tmp/corpus/ngrams/pentagrams  -file /stage/AIU/corpus/mapper_create_fiveGrams.py -mapper mapper_create_fiveGrams.py  -file /stage/AIU/corpus/reducer_create_nGrams.py -reducer reducer_create_nGrams.py -file /stage/AIU/corpus/profanity_words.txt 

8.3 Create an Imapala table with the unigram output location. Will be useful for sanity check.
impala-shell -i IP:PORT -d DBNAME
CREATE EXTERNAL TABLE PENTAGRAMS
(
   NGRAMS STRING,
   FREQ INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/tmp/corpus/ngrams/pentagrams';

INVALIDATE METADATA;

8.4 Checking
impala> select count(*) from PENTAGRAMS;
impala> select count(distinct NGRAMS) from PENTAGRAMS;

# hadoop fs -cat /tmp/corpus/ngrams/pentagrams/*|wc -l

Above 3 command should have same output(in this case 50545866)


9. Do word indexing with interger numbers.
9.1 run the reduceonly job (map job just emits all the keys). Make sure to put "-numReduceTasks 1" other wise indexing will be incorrect. Use unigrams as input.
hadoop fs -rm -r -skipTrash /tmp/corpus/ngrams/wordidx
hadoop jar $HADOOP_STREAMING -input /tmp/corpus/ngrams/unigrams/* -output /tmp/corpus/ngrams/wordidx  -file /stage/AIU/corpus/mapper_word_indexer.py -mapper mapper_word_indexer.py  -file /stage/AIU/corpus/reducer_word_indexer.py -reducer reducer_word_indexer.py -numReduceTasks 1

9.2 Create an Imapla table
impala-shell -i IP:PORT -d DBNAME
CREATE EXTERNAL TABLE WORDIDX
(
   NGRAMS STRING,
   IDX INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/tmp/corpus/ngrams/wordidx';

INVALIDATE METADATA;

9.3 checking
impala> select count(*) from WORDIDX;
998416
impala> select count(distinct NGRAMS) from WORDIDX;
998416
impala> select count(distinct IDX),max(IDX),min(IDX) from WORDIDX;
998416,998416,1

# hadoop fs -cat /tmp/corpus/ngrams/wordidx/*|wc -l
998416

Above should be showing counts equal to unigrams.

9.4 Export the word index file out of HDFS
hadoop fs -cat /tmp/corpus/ngrams/wordidx/* >> wordidx.csv

9.5 now convert the csv to JOSN to use for convert other ngrams by python
./jsonConverter.py wordidx.csv wordidx.json


10. Convert bigrams to numeric indexes, it will be a maponly job. donot forget to put "wordidx.json" in -file parameter, as python program will read this.

10.1 run the maponly job
hadoop fs -rm -r -skipTrash /tmp/corpus/indexedngrams/bigrams
hadoop jar $HADOOP_STREAMING -input /tmp/corpus/ngrams/bigrams/* -output /tmp/corpus/indexedngrams/bigrams  -file /stage/AIU/corpus/mapper_bigramCompressor.py -mapper mapper_bigramCompressor.py  -file /stage/AIU/corpus/wordidx.json

10.2 create an inpala table with the above output location
impala-shell -i IP:PORT -d DBNAME
CREATE EXTERNAL TABLE BIGRAMIDX
(
   FREQ INT,
   WORDIDX1 INT,
   WORDIDX2 INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/tmp/corpus/indexedngrams/bigrams';

INVALIDATE METADATA;

10.3 checking
impala> select count(*) from BIGRAMIDX;
13203263
impala> select min(FREQ),MAX(FREQ),min(WORDIDX1),max(WORDIDX1),min(WORDIDX2),max(WORDIDX2) from BIGRAMIDX;
+-----------+-----------+---------------+---------------+---------------+---------------+
| min(freq) | max(freq) | min(wordidx1) | max(wordidx1) | min(wordidx2) | max(wordidx2) |
+-----------+-----------+---------------+---------------+---------------+---------------+
| 1         | 422318    | 1             | 998410        | 1             | 998416        |
+-----------+-----------+---------------+---------------+---------------+---------------+

# hadoop fs -cat /tmp/corpus/indexedngrams/bigrams/*|wc -l

11. Convert trigrams to numeric indexes, it will be a maponly job. donot forget to put "wordidx.json" in -file parameter, as python program will read this.

11.1 run the map only job
hadoop fs -rm -r -skipTrash /tmp/corpus/indexedngrams/trigrams
hadoop jar $HADOOP_STREAMING -input /tmp/corpus/ngrams/trigrams/* -output /tmp/corpus/indexedngrams/trigrams  -file /stage/AIU/corpus/mapper_trigramCompressor.py -mapper mapper_trigramCompressor.py  -file /stage/AIU/corpus/wordidx.json

11.2 create a impala table piunting to above output location
impala-shell -i IP:PORT -d DBNAME
CREATE EXTERNAL TABLE TRIGRAMIDX
(
   FREQ INT,
   WORDIDX1 INT,
   WORDIDX2 INT,
   WORDIDX3 INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/tmp/corpus/indexedngrams/trigrams';

INVALIDATE METADATA;

11.3 checking
impala> select count(*) from TRIGRAMIDX;
35769259
impala> select min(FREQ),MAX(FREQ),min(WORDIDX1),max(WORDIDX1),min(WORDIDX2),max(WORDIDX2),min(WORDIDX3),max(WORDIDX3) from TRIGRAMIDX;
+-----------+-----------+---------------+---------------+---------------+---------------+---------------+---------------+
| min(freq) | max(freq) | min(wordidx1) | max(wordidx1) | min(wordidx2) | max(wordidx2) | min(wordidx3) | max(wordidx3) |
+-----------+-----------+---------------+---------------+---------------+---------------+---------------+---------------+
| 1         | 28983     | 1             | 998410        | 1             | 998410        | 1             | 998416        |
+-----------+-----------+---------------+---------------+---------------+---------------+---------------+---------------+


# hadoop fs -cat /tmp/corpus/indexedngrams/trigrams/*|wc -l

12. convert quadgrams to numeric indexes, it will be a maponly job. donot forget to put "wordidx.json" in -file parameter, as python program will read this.

12.1 Run the maponly job
hadoop fs -rm -r -skipTrash /tmp/corpus/indexedngrams/quadgrams
hadoop jar $HADOOP_STREAMING -input /tmp/corpus/ngrams/quadgrams/* -output /tmp/corpus/indexedngrams/quadgrams  -file /stage/AIU/corpus/mapper_quadgramCompressor.py -mapper mapper_quadgramCompressor.py  -file /stage/AIU/corpus/wordidx.json

12.2 Create an impala table with above output location
impala-shell -i IP:PORT -d DBNAME 
CREATE EXTERNAL TABLE QUADGRAMIDX
(
   FREQ INT,
   WORDIDX1 INT,
   WORDIDX2 INT,
   WORDIDX3 INT,
   WORDIDX4 INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/tmp/corpus/indexedngrams/quadgrams';

INVALIDATE METADATA;

12.3 do some checking
impala> select count(*) from QUADGRAMIDX;
49768190
impala> select min(FREQ),MAX(FREQ),min(WORDIDX1),max(WORDIDX1),min(WORDIDX2),max(WORDIDX2),min(WORDIDX3),max(WORDIDX3),min(WORDIDX4),max(WORDIDX4) from QUADGRAMIDX;
+-----------+-----------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| min(freq) | max(freq) | min(wordidx1) | max(wordidx1) | min(wordidx2) | max(wordidx2) | min(wordidx3) | max(wordidx3) | min(wordidx4) | max(wordidx4) |
+-----------+-----------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| 1         | 7466      | 1             | 998410        | 1             | 998410        | 1             | 998410        | 1             | 998416        |
+-----------+-----------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+


# hadoop fs -cat /tmp/corpus/indexedngrams/quadgrams/*|wc -l


13. convert pentagrams to numeric indexes, it will be a maponly job. donot forget to put "wordidx.json" in -file parameter, as python program will read this.

13.1 run the maponly job
hadoop fs -rm -r -skipTrash /tmp/corpus/indexedngrams/pentagrams
hadoop jar $HADOOP_STREAMING -input /tmp/corpus/ngrams/pentagrams/* -output /tmp/corpus/indexedngrams/pentagrams  -file /stage/AIU/corpus/mapper_pentagramCompressor.py -mapper mapper_pentagramCompressor.py  -file /stage/AIU/corpus/wordidx.json

13.2 create impala table
impala-shell -i IP:PORT -d DBNAME 
CREATE EXTERNAL TABLE PENTAGRAMIDX
(
   FREQ INT,
   WORDIDX1 INT,
   WORDIDX2 INT,
   WORDIDX3 INT,
   WORDIDX4 INT,
   WORDIDX5 INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/tmp/corpus/indexedngrams/pentagrams';

INVALIDATE METADATA;

13.3 checking
impala> select count(*) from PENTAGRAMIDX;
50545866
impala> select min(FREQ),MAX(FREQ),min(WORDIDX1),max(WORDIDX1),min(WORDIDX2),max(WORDIDX2),min(WORDIDX3),max(WORDIDX3),min(WORDIDX4),max(WORDIDX4),min(WORDIDX5),max(WORDIDX5) from PENTAGRAMIDX;
[IP:PORT] > select min(FREQ),MAX(FREQ),min(WORDIDX1),max(WORDIDX1),min(WORDIDX2),max(WORDIDX2),min(WORDIDX3),max(WORDIDX3),min(WORDIDX4),max(WORDIDX4),min(WORDIDX5),max(WORDIDX5) from PENTAGRAMIDX;
Query: select min(FREQ),MAX(FREQ),min(WORDIDX1),max(WORDIDX1),min(WORDIDX2),max(WORDIDX2),min(WORDIDX3),max(WORDIDX3),min(WORDIDX4),max(WORDIDX4),min(WORDIDX5),max(WORDIDX5) from PENTAGRAMIDX
+-----------+-----------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| min(freq) | max(freq) | min(wordidx1) | max(wordidx1) | min(wordidx2) | max(wordidx2) | min(wordidx3) | max(wordidx3) | min(wordidx4) | max(wordidx4) | min(wordidx5) | max(wordidx5) |
+-----------+-----------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| 1         | 2848      | 1             | 998410        | 1             | 998410        | 1             | 998410        | 1             | 998410        | 1             | 998413        |
+-----------+-----------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
Fetched 1 row(s) in 1.48s



# hadoop fs -cat /tmp/corpus/indexedngrams/pentagrams/*|wc -l
50545866:1850
49768190:1450
35769259: 815
13203263: 215

14. select the approipriate size for final ngrams:
14.1 fix howmant records will be taken. [filesize*totalcount/(count with freq filter)]
impala-shell -i IP:PORT -d DBNAME 
select 215*count(*)/13203263,count(*) from BIGRAMIDX where FREQ > 4;		: 22MB	: 1378101
select 815*count(*)/35769259,count(*) from TRIGRAMIDX where FREQ > 5;		: 30MB	: 1268894
select 1450*count(*)/49768190,count(*) from QUADGRAMIDX where FREQ > 4; 	: 22MB 	: 775446
select 1850*count(*)/50545866,count(*) from PENTAGRAMIDX where FREQ > 2; 	: 25MB 	: 701336

14.2 Export final reduced size ngrams using impala, so that we can use R:

impala-shell -i IP:PORT -B --output_delimiter "," --print_header -d "AXDB" -q "select FREQ,WORDIDX1,WORDIDX2 from BIGRAMIDX where FREQ > 4;" > /stage/AIU/corpus/indexedBigrams.csv

impala-shell -i IP:PORT -B --output_delimiter "," --print_header -d "AXDB" -q "select FREQ,WORDIDX1,WORDIDX2,WORDIDX3 from TRIGRAMIDX where FREQ > 5;" > /stage/AIU/corpus/indexedTrigrams.csv

impala-shell -i IP:PORT -B --output_delimiter "," --print_header -d "AXDB" -q "select FREQ,WORDIDX1,WORDIDX2,WORDIDX3,WORDIDX4 from QUADGRAMIDX where FREQ > 4;" > /stage/AIU/corpus/indexedQuadgrams.csv

impala-shell -i IP:PORT -B --output_delimiter "," --print_header -d "AXDB" -q "select FREQ,WORDIDX1,WORDIDX2,WORDIDX3,WORDIDX4,WORDIDX5 from PENTAGRAMIDX where FREQ > 2;" > /stage/AIU/corpus/indexedPentagrams.csv

Note: Better, remove the header again, as this impala export has some extra chars at the neginning

14.3  minize the size of word dict with the word used in ngrams [2,3,4 & 5 grams]
impala-shell -i IP:PORT -d DBNAME 
create table uniqGrams as
select WORDIDX1 IDX from BIGRAMIDX where FREQ > 4
union
select WORDIDX2 from BIGRAMIDX where FREQ > 4
union 
select WORDIDX1 from TRIGRAMIDX where FREQ > 5
union 
select WORDIDX2 from TRIGRAMIDX where FREQ > 5
union 
select WORDIDX3 from TRIGRAMIDX where FREQ > 5
union 
select WORDIDX1 from QUADGRAMIDX where FREQ > 4
union 
select WORDIDX2 from QUADGRAMIDX where FREQ > 4
union 
select WORDIDX3 from QUADGRAMIDX where FREQ > 4
union 
select WORDIDX4 from QUADGRAMIDX where FREQ > 4
union 
select WORDIDX1 from PENTAGRAMIDX where FREQ > 2
union 
select WORDIDX2 from PENTAGRAMIDX where FREQ > 2
union 
select WORDIDX3 from PENTAGRAMIDX where FREQ > 2
union 
select WORDIDX4 from PENTAGRAMIDX where FREQ > 2
union 
select WORDIDX5 from PENTAGRAMIDX where FREQ > 2;

create table finalDict as
select A.NGRAMS, A.IDX from WORDIDX A, uniqGrams B where A.IDX=B.IDX;

select count(*) from finalDict;
select count(*) from uniqGrams;

impala-shell -i IP:PORT -B --output_delimiter "," --print_header -d "AXDB" -q "select NGRAMS,IDX from finalDict;" > /stage/AIU/corpus/finalwordidx.csv

15. Preprocess these files in R to use in Shiny 

15.1 find the most Frequent 3 words witch will be used as default starting prediction
impala-shell -i IP:PORT -d DBNAME 
>select * from UNIGRAMS order by freq desc limit 3;
Query: select * from UNIGRAMS order by freq desc limit 3
+--------+---------+
| ngrams | freq    |
+--------+---------+
| the    | 4225336 |
| to     | 2714376 |
| and    | 2286862 |
+--------+---------+


Note: For below steps, use uncommon na string to keep the string as it is, other wise NA will be treated as not available
15.2 convert the word dictionary to RDS
wordDict <- read.csv("./finalNGrams/finalwordidx.csv", na.strings = "##NaN##", header=FALSE)
names(wordDict) <- c("words", "idx")
saveRDS(wordDict, file="./finalNGrams/unigramsidx.rds")

15.3 convet the word biGrams to RDS
biGrams <- read.csv("./finalNGrams/indexedBiGrams.csv", na.strings = "##NaN##", header=FALSE)
names(biGrams) <- c("freq", "wordIdx1", "wordIdx2")
saveRDS(biGrams, file="./finalNGrams/indexedBiGrams.rds")

15.4 convet the word triGrams to RDS
triGrams <- read.csv("./finalNGrams/indexedTriGrams.csv", na.strings = "##NaN##", header=FALSE)
names(triGrams) <- c("freq", "wordIdx1", "wordIdx2", "wordIdx3")
saveRDS(triGrams, file="./finalNGrams/indexedTriGrams.rds") 

15.5 convet the word quadGrams to RDS
quadGrams <- read.csv("./finalNGrams/indexedQuadGrams.csv", na.strings = "##NaN##", header=FALSE)
names(quadGrams) <- c("freq", "wordIdx1", "wordIdx2", "wordIdx3", "wordIdx4")
saveRDS(quadGrams, file="./finalNGrams/indexedQuadGrams.rds") 

15.6 convet the word pentaGrams to RDS
pentaGrams <- read.csv("./finalNGrams/indexedPentaGrams.csv", na.strings = "##NaN##", header=FALSE)
names(pentaGrams) <- c("freq", "wordIdx1", "wordIdx2", "wordIdx3", "wordIdx4", "wordIdx5")
saveRDS(pentaGrams, file="./finalNGrams/indexedPentaGrams.rds") 
