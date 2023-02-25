# Hive in GCP

The GCP service that includes Hive (and Hadoop and Spark) is called DataProc. To launch it and use it, you need to

1. Obtain a Cluster [as for Hadoop](https://github.com/singhj/big-data-repo/blob/main/hadoop/hadoop_in_gcp.md),
2. `ssh` into the cluster master,
3. Stage input files onto the cluster master, 
```
    git clone https://github.com/singhj/big-data-repo.git
```
4. Move input files into HDFS,
```
    hadoop fs -mkdir /user/singhj
    hadoop fs -mkdir /user/singhj/five-books
    # Move input files into HDFS
    hadoop fs -put ~/big-data-repo/five-books/* /user/singhj/five-books
    # Verify that the files got there
    hadoop fs -ls /user/singhj/five-books
    Found 5 items
    -rw-r--r--   1 j_singh hadoop     179903 2023-02-08 20:18 /user/singhj/five-books/a_tangled_tale.txt
    -rw-r--r--   1 j_singh hadoop     173379 2023-02-08 20:18 /user/singhj/five-books/alice_in_wonderland.txt
    -rw-r--r--   1 j_singh hadoop     394246 2023-02-08 20:18 /user/singhj/five-books/sylvie_and_bruno.txt
    -rw-r--r--   1 j_singh hadoop     458755 2023-02-08 20:18 /user/singhj/five-books/symbolic_logic.txt
    -rw-r--r--   1 j_singh hadoop     135443 2023-02-08 20:18 /user/singhj/five-books/the_game_of_logic.txt
```
5. Run Word Count
```
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar wordcount /user/books /user/j_singh/books-count-hive
    hadoop fs -ls /user/j_singh/books-count-hive
```

6. Invoke hive from the command line by typing `hive`

```
    Hive Session ID = 16f9450f-0059-487c-9706-ea02a6b02932

    Logging initialized using configuration in file:/etc/hive/conf.dist/hive-log4j2.properties Async: true
    Hive Session ID = 3f159de0-7408-4734-90b5-7bc45338e504
```
7. Declare an external table `bookscount` that binds to the contents of the directory `/user/j_singh/books-count-hive`
```
    OK
    Time taken: 1.735 seconds
    hive > CREATE EXTERNAL TABLE bookscount (word string, count int) \
               ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LOCATION '/user/j_singh/books-count';   
```
8. Bind `bookscount` table metadata to `/user/j_singh/books-count`

Runs a SQL-like Query. It invokes mapreduce jobs as needed
```
    SELECT word, count FROM bookscount where count > 2000 SORT BY count DESC;

    Query ID = j_singh_20230224231421_d76f7158-ad49-46a4-a11e-ddb4bc7c8248
    Total jobs = 1
    Launching Job 1 out of 1
    Status: Running (Executing on YARN cluster with App id application_1677262538403_0004)

    ----------------------------------------------------------------------------------------------
            VERTICES      MODE        STATUS  TOTAL  COMPLETED  RUNNING  PENDING  FAILED  KILLED  
    ----------------------------------------------------------------------------------------------
    Map 1 .......... container     SUCCEEDED      1          1        0        0       0       0  
    Reducer 2 ...... container     SUCCEEDED      1          1        0        0       0       0  
    ----------------------------------------------------------------------------------------------
    VERTICES: 02/02  [==========================>>] 100%  ELAPSED TIME: 10.37 s    
    ----------------------------------------------------------------------------------------------
```
The returned answer is:
```
    the     9454
    |       7243
    of      4795
    to      4732
    and     4158
    a       3954
    are     3255
    in      2657
    I       2123
    Time taken: 14.156 seconds, Fetched: 9 row(s)
hive> 
```

