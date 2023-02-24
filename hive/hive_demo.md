# Hive in GCP

The GCP service that includes Hive (and Hadoop and Spark) is called DataProc. To launch it and use it, you need to

1. Obtain a Cluster [as for Hadoop](https://github.com/singhj/big-data-repo/blob/main/hadoop/hadoop_in_gcp.md),
2. `ssh` into the cluster master,
3. Stage input files onto the cluster master, 
4. Move input files into HDFS,

## Move Input Files to HDFS

To move files on Cluster Master, into HDFS, use `hadoop fs -put ~/big-data-repo/five-books /user/singhj/five-books` 

    git clone https://github.com/singhj/big-data-repo.git
    hadoop fs -mkdir /user/singhj
    hadoop fs -mkdir /user/singhj/five-books                             # create directory five-books in HDFS
    hadoop fs -put ~/big-data-repo/five-books/* /user/singhj/five-books  # put the contents of five-books into HDFS

Verify that the files got there:

    hadoop fs -ls /user/singhj/five-books

```
Found 5 items
-rw-r--r--   1 j_singh hadoop     179903 2023-02-08 20:18 /user/singhj/five-books/a_tangled_tale.txt
-rw-r--r--   1 j_singh hadoop     173379 2023-02-08 20:18 /user/singhj/five-books/alice_in_wonderland.txt
-rw-r--r--   1 j_singh hadoop     394246 2023-02-08 20:18 /user/singhj/five-books/sylvie_and_bruno.txt
-rw-r--r--   1 j_singh hadoop     458755 2023-02-08 20:18 /user/singhj/five-books/symbolic_logic.txt
-rw-r--r--   1 j_singh hadoop     135443 2023-02-08 20:18 /user/singhj/five-books/the_game_of_logic.txt
```

## Run Word Count
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar wordcount /user/books /user/j_singh/books-count
hadoop fs -ls /user/j_singh/books-count

### In hive:

Bind table metadata to word count data
```
CREATE EXTERNAL TABLE bookscount (word string, count int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LOCATION '/user/j_singh/books-count';   
```
Query, invoking mapreduce jobs as needed
```
SELECT word, count FROM bookscount where count > 2000 SORT BY count DESC;
```
