# Hadoop in GCP

The GCP service that includes Hadoop (and Spark) is called DataProc. To launch it and use it, you need to

1. Obtain a Cluster,
    * specify where (i.e., what region) it should run,
    * how many workers is should have (in additional to the master),
    * the type of CPU the master should be, and with how much memory and storage
    * the type of CPU the workers should be, and with how much memory and storage
2. `ssh` into the cluster master,
3. Stage input files onto the cluster master, 
4. Move input files into HDFS,
5. Verify that the default (prepackaged) Hadoop runs without errors,
6. Verify that Hadoop Streaming, written with your own mapper but the default reducer, runs without errors,
7. Replace the default reducer with your own reducer and verify that it works without errors.

Once you have gone through these steps, you will have created a *baseline configuration* and return to it when something goes awry and you need to begin again!

## Obtain a Cluster

1. Visit https://console.cloud.google.com/dataproc/
    * If you aren't already logged in, please log into your Google account
    * Your project should already be chosen
    * ![](https://raw.githubusercontent.com/singhj/big-data-repo/main/hadoop/images/start_dataproc.png)
    * Click on CREATE CLUSTER
    * This [page](https://cloud.google.com/blog/topics/training-certifications/new-trainings-teach-you-the-basics-of-architecting-on-google-cloud) explains the options the next screene presents. choose Cluster on Compute Engine. 
     ![](https://raw.githubusercontent.com/singhj/big-data-repo/main/hadoop/images/create_dataproc_cluster.png)
    * specify where (i.e., what region) it should run,
    * how many workers is should have (in additional to the master),
    * under **Configure Nodes** (optional),
        * the type of CPU the master should be, and with how much memory and storage
        * the type of CPU the workers should be, and with how much memory and storage
    ![](https://raw.githubusercontent.com/singhj/big-data-repo/main/hadoop/images/specify_cluster.png)

    Finally, click on Create.

## `ssh` into the cluster master,

Once the cluster has been launched, it will show up under Clusters

![](https://raw.githubusercontent.com/singhj/big-data-repo/main/hadoop/images/running_clusters_in_dataproc.png)

1. Click on the cluster name.
2. Switch to the ‘VM instances’ tab.
3. The drop-down near SSH shows options for  accessing the cluster master machine
    ![](https://raw.githubusercontent.com/singhj/big-data-repo/main/hadoop/images/ssh_into_cluster_master.png)
    * At first, the SSH is disabled. 
    * Wait for it to become “live.”
    * Click on SSH when it is enabled. (If in doubt, choose ‘Open in a Browser Window’)
    * This opens a bash (linux) shell into the master machine.

Staging Input Files
There are multiple systems involved. Always be aware of where you are:

What machine are you on?
What is your current directory?
What system are you using?
Use gsutil cp (or cURL, or git clone, etc.) to bring files to the Cluster Master, for example,

git clone https://github.com/singhj/big-data-repo.git

## Moving Files to HDFS

To move files on Cluster Master, into HDFS, use `hadoop fs -put ~/big-data-repo/five-books /user/singhj/five-books` 

    hadoop fs -mkdir  /user/singhj/five-books            # create directory five-books in HDFS
    hadoop fs -put five-books/* /user/singhj/five-books  # put the contents of five-books into HDFS

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
## Running the pre-packaged Hadoop Wordcount

The objective of this step is to verify that we have a good installation of `hadoop`. If this step doesn't work, pause and correct the error before proceeding.

The command is

    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar wordcount /user/singhj/five-books /books-count

Hadoop uses hdfs as its (distributed) file system. The directory /books-count is created by the above command and must not already exist!

Once it has run, copy the contents of /books-count to the cluster master and examine them

```
hadoop fs -get /books-count
ls -la books-count/
total 316
drwxr-xr-x 2 j_singh j_singh   4096 Sep 27 15:48 .
drwxr-xr-x 6 j_singh j_singh   4096 Sep 27 15:48 ..
-rw-r--r-- 1 j_singh j_singh      0 Sep 27 15:48 _SUCCESS
-rw-r--r-- 1 j_singh j_singh 313829 Sep 27 15:48 part-r-00000
```
Depending on the configuration and the problem, you may get just one `part-r-00000` or many `part-r-00000` files.


## Writing our own mapper

The objective of this step is to verify that hadoop streaming is properly installed. If this step doesn't work, pause and correct the error before proceeding.

Mapper code is

```
#!/usr/bin/env python
import sys, re

def main(argv):
    line = sys.stdin.readline()
    pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
    try:
        while line:
            for word in pattern.findall(line):
                print ("LongValueSum:" + word.lower() + "\t" + "1")
            line = sys.stdin.readline()
    except EOFError as error:
        return None

if __name__ == "__main__":
    main(sys.argv)

```

To run it,
```
mapred streaming -input myInputDirs -output myOutputDir \
  -file myPythonScript.py -mapper myPythonScript.py \
  -reducer aggregate
```
The directory myOutputDir is created by the above command and must not already exist! The `mapred` command will fail if the output directory exists. Often you can just rerun the command with a different directory name

After execution, copy the contents of myOutputDir to the cluster master with
```
hadoop fs -get myOutputDir 
```

**And don’t forget to delete the cluster at the end!**

As before, depending on the configuration and the problem, you may get just one `part-r-00000` or many `part-r-00000` files.

## Common Errors

Students have run into the following hurdles in the past:

* **Versions.** Make sure that your documentation on the web corresponds to the version of your Hadoop

```
    j_singh@cluster-8bca-m:~$ hadoop version
    Hadoop 3.2.3
```
*    **Line endings.** Program files that were created on Windows machines often have Windows-style line endings that Hadoop doesn’t like. [Here](https://www.maketecheasier.com/convert-files-from-linux-format-windows/) are some ways of fixing it.



A
A
A
B
B
B
B
B
B
B
B
B
B
B
B
The books files are now on the cluster master.

