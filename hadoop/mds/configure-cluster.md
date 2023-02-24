# Hadoop in GCP

The GCP service that includes Hadoop (and Spark) is called DataProc. To launch it and use it, you need to

1. Obtain a Cluster by visiting <a href="https://console.cloud.google.com/dataproc/" target="_blank">Google DataProc</a> and clicking on CREATE CLUSTER.
    * specify where (i.e., what region) it should run,
    * how many workers is should have (in additional to the master),
    * the type of CPU the master should be, and with how much memory and storage
    * the type of CPU the workers should be, and with how much memory and storage

## Visit https://console.cloud.google.com/dataproc/
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

