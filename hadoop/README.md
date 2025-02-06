# Hadoop in GCP

The GCP service that includes Hadoop (and Spark) is called DataProc. To launch it and use it, we need to

1. Obtain a Cluster,
    * specify where (i.e., what region) it should run,
    * how many workers is should have (in additional to the master),
    * the type of CPU the master should be, and with how much memory and storage
    * the type of CPU the workers should be, and with how much memory and storage
2. `ssh` into the cluster master,
3. Stage input files onto the cluster master, 
4. Move input files into HDFS,
5. Verify that the default (prepackaged) Hadoop runs without errors,
6. Verify that Hadoop Streaming, written with our own mapper but the default reducer, runs without errors,
7. Replace the default reducer with your own reducer and verify that it works without errors.

This is how we can return to a baseline when something goes awry and we need to start afresh!

## Obtain a Cluster

1. Visit https://console.cloud.google.com/dataproc/
    * If you aren't already logged in, please log into your Google account
    * Your project should already be chosen
    * ![](https://raw.githubusercontent.com/singhj/big-data-repo/main/hadoop/images/start_dataproc.png)
    * Click on CREATE CLUSTER
    * This [page](https://cloud.google.com/blog/topics/training-certifications/new-trainings-teach-you-the-basics-of-architecting-on-google-cloud) explains the options the next screen presents.
    Choose <i>Cluster on Compute Engine</i>. 
     ![](https://raw.githubusercontent.com/singhj/big-data-repo/main/hadoop/images/create_dataproc_cluster.png)
    * specify where (i.e., what region) it should run,
    * how many workers is should have (in additional to the master),
    * under **Configure Nodes** (optional),
        * the type of CPU the master should be, and with how much memory and storage
        * the type of CPU the workers should be, and with how much memory and storage
    ![](https://raw.githubusercontent.com/singhj/big-data-repo/main/hadoop/images/specify_cluster.png)

    * under **Customize cluster** (optional), **(this is not optional!)**, uncheck the checkbox for Internal IP only. Otherwise you won't be able to `ssh` into the cluster master (our next step)!
    ![](https://raw.githubusercontent.com/singhj/big-data-repo/main/hadoop/images/uncheck_internal_IP_only.png)

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
    * Run `hadoop version` in the shell to determine the version. (On 2/24/23, it was Hadoop 3.2.3. Make sure to consult documentation for [that version](https://hadoop.apache.org/docs/r3.2.3/hadoop-streaming/HadoopStreaming.html)


## Stage Input Files
There are multiple systems involved. Always be aware of where you are:

* What machine are you on?
* What is your current directory?
* Use `gsutil cp` (or `cURL`, or `git clone`, etc.) to bring files to the Cluster Master, for example,
```
# Bring books files from Github to the Cluster Master
git clone https://github.com/singhj/big-data-repo.git
```

## Move books Files to HDFS

To move files on Cluster Master, into HDFS, use `hadoop fs -put ~/big-data-repo/five-books /user/jitendra_singh/five-books`, but first create a directory `/user/jitendra_singh/five-books` in HDFS for them.

    hadoop fs -mkdir /user/jitendra_singh
    hadoop fs -mkdir /user/jitendra_singh/five-books                             # create directory five-books in HDFS
    hadoop fs -put ~/big-data-repo/five-books/* /user/jitendra_singh/five-books  # put the contents of five-books into HDFS

Verify that the files got there:

    hadoop fs -ls /user/jitendra_singh/five-books

```
Found 5 items
-rw-r--r--   1 jitendra_singh hadoop     179903 2023-02-08 20:18 /user/jitendra_singh/five-books/a_tangled_tale.txt
-rw-r--r--   1 jitendra_singh hadoop     173379 2023-02-08 20:18 /user/jitendra_singh/five-books/alice_in_wonderland.txt
-rw-r--r--   1 jitendra_singh hadoop     394246 2023-02-08 20:18 /user/jitendra_singh/five-books/sylvie_and_bruno.txt
-rw-r--r--   1 jitendra_singh hadoop     458755 2023-02-08 20:18 /user/jitendra_singh/five-books/symbolic_logic.txt
-rw-r--r--   1 jitendra_singh hadoop     135443 2023-02-08 20:18 /user/jitendra_singh/five-books/the_game_of_logic.txt
```
## Running the pre-packaged Hadoop Wordcount

The objective of this step is to verify that we have a good installation of `hadoop`. If this step doesn't work, pause and correct the error before proceeding.

The command is

    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar wordcount /user/jitendra_singh/five-books /books-count-0

Hadoop uses hdfs as its (distributed) file system. The directory /books-count-0 is created by the above command and must not already exist! *If the above command needs to be rerun, either delete the directory or change the command to write to a different directory, say `/books-count-1`*

Once it has run, copy the contents of /books-count-0 to the cluster master and examine them

```
hadoop fs -get /books-count-0

ls -la books-count-0
```

```
total 316
drwxr-xr-x 2 jitendra_singh jitendra_singh   4096 Sep 27 15:48 .
drwxr-xr-x 6 jitendra_singh jitendra_singh   4096 Sep 27 15:48 ..
-rw-r--r-- 1 jitendra_singh jitendra_singh      0 Sep 27 15:48 _SUCCESS
-rw-r--r-- 1 jitendra_singh jitendra_singh 313829 Sep 27 15:48 part-r-00000
```

Depending on the configuration and the problem, you may get an arbitrary number of `part-r-0000*` files.


## Writing our own mapper

We will use Hadoop Streaming for this. Hadoop Streaming fits into the Hadoop architecture as shown below:
![](https://raw.githubusercontent.com/singhj/big-data-repo/main/hadoop/images/mrs5.png). Courtesy, <a href="https://nancyyanyu.github.io/posts/f53c188b/">Nancy Yanyu</a>

Hadoop Streaming provides hooks for plugging in your own mapper and reducer into Hadoop. The mapper hook sends 
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

To use it, execute
```
mapred streaming -files /home/jitendra_singh/big-data-repo/hadoop/mapper_noll.py \
                 -mapper /home/jitendra_singh/big-data-repo/hadoop/mapper_noll.py \
                 -input /user/jitendra_singh/five-books \
                 -reducer aggregate \
                 -output /books-count-m-0
```
**Explanation**: the command line arguments should be interpreted as follows. More details [here](https://hadoop.apache.org/docs/r3.2.3/hadoop-streaming/HadoopStreaming.html#Streaming_Command_Options).

| Argument   | Explanation |
|:-----------|-------------|
| `-files    | The absolute pathname of the files on the cluster master. <br/>Make the file (mapper, reducer, or combiner executable) available locally on each worker node |
| `-mapper`  | The name of the mapper file, `mapper_noll.py` in this case |
| `-reducer` | The name of the reducer file, `aggregate` for now (default hadoop reducer) |
| `-input`   | The HDFS pathname of the directory that holds the input files. <br/>The files must already be in HDFS. |
| `-output`  | The HDFS pathname of the directory that will hold the output files. <br/>The directory is created by the command. |


The directory `/books-count-m-0` is created in HDFS by the above command and must not already exist! The `mapred` command will fail if the output directory exists. Often you can just rerun the command with a different directory name

After execution, copy the contents of `/books-count-m-0` to the cluster master with
```
hadoop fs -get /books-count-m-0
```
## Writing our own reducer

The Michael Noll reducer is available in `~/big-data-repo/hadoop/reducer_noll.py`

To use it, execute
```
mapred streaming -files /home/jitendra_singh/big-data-repo/hadoop/mapper_noll.py,/home/jitendra_singh/big-data-repo/hadoop/reducer_noll.py \
                 -mapper  /home/jitendra_singh/big-data-repo/hadoop/mapper_noll.py \
                 -reducer /home/jitendra_singh/big-data-repo/hadoop/reducer_noll.py \
                 -input /user/jitendra_singh/five-books \
                 -output /books-counts-mr-0
```
After execution, copy the contents of `/books-counts-mr-0` as before.

**And don’t forget to delete the cluster at the end!**

As before, depending on the configuration and the problem, you may get just one `part-r-00000` or many `part-r-00000` files.

## Common Errors

Students have run into the following hurdles in the past:

* **Versions.** Make sure that your documentation on the web corresponds to the version of your Hadoop. The next few lines
provide the version info on what was running in GCP in Feb 2025.

```
jitendra_singh@cluster-e140-m:~$ hadoop version
    Hadoop 3.3.6
    Source code repository https://bigdataoss-internal.googlesource.com/third_party/apache/hadoop -r 504ae3bf1cb5506ac7e651ef8de5a1fb88e9ce73
    Compiled by bigtop on 2025-01-23T21:16Z
    Compiled on platform linux-x86_64
    Compiled with protoc 3.7.1
    From source with checksum 1c64772fae4e6cb4d3f95a08473ed58
    This command was run using /usr/lib/hadoop/hadoop-common-3.3.6.jar
```
*    **Line endings.** Program files that were created on Windows machines often have Windows-style line endings that Hadoop doesn’t like. [Here](https://www.maketecheasier.com/convert-files-from-linux-format-windows/) are some ways of fixing it.



