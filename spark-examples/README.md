# Spark Structured Streaming Demo

This demo can be run in a Dataproc cluster ***or*** on the Halligan servers at Tufts.

If using the Dataproc cluster, *under-powered configurations may fail in mysterious ways*. However, everything works with these settings:
1. **Set up Cluster:** Single Node (1 master, 0 workers)
2. **Configure nodes:**
    * Machine series: N2,
    * machine type: n2-standard-4 (4 vCPU, 2 core, 16 GB memory),
    * Primary disk size: 1200 GB,
    * Primary disk type: Standard Persistent Disk
3. **Customize cluster:** Under Internal IP only, uncheck *Configure all instances to have only internal IP addresses*

## Steps:

1. Log into master machine of the cluster (or open a terminal into a Halligan server).
2. Git clone my repo: `git clone https://github.com/singhj/big-data-repo.git`
3. Install `tqdm`: `sudo apt install python3-tqdm`. `sudo` is disallowed on the Halligan servers. Instead, use `pip3 install tqdm`.
4. Install `nltk`: `sudo apt install python3-nltk`. `sudo` is disallowed on the Halligan servers. Instead, use `pip3 install nltk`.
5. Set the `PATH` environment variable: `PATH="$PATH:$HOME/big-data-repo/:$HOME/big-data-repo/spark-examples/"`
6. Install `pip` if necessary: `sudo apt install python3-pip`
7. Pandas is no longer pre-installed on GCP clusters. Use `sudo apt install python3-pandas` to install it.
8. Use `sudo apt install python3-numpy` to install Numpy if it isn't already available on the GCP master.
6. Test `netcat`:
    * Start a second (listener) shell. (Or open a second terminal window into the Halligan server to do this).
    * In the first (sender shell), set up sender: `nc -lk 9999`
    * In the listener shell, `nc localhost 9999`
    * Any words typed into the sender shell should appear in the listener shell.
    * Stop `netcat` in both shells by hitting `^C`
7. Set up `netcat` pipeline for inaugural speeches:
    * In the sender shell, `inaugural-speech-feeder.py | nc -lk 9999`. You have about 30 seconds to start the listener (the next step).
    * In the listener shell, `nc localhost 9999`
    * If it worked, you should see the inaugural speeches appear in the listener.
    * Stop `netcat` in both shells by hitting `^C`
8. Set up wordcount pipeline:
    * In the sender shell, `inaugural-speech-feeder.py | nc -lk 9999`. You have about 30 seconds to start the listener (the next step).
    * In the listener shell, `spark-submit ~/big-data-repo/spark-examples/structured-network-wordcount.py localhost 9999`
    * If it worked, you should see wordcounts for the inaugural speeches appear in the listener.
    * Stop `netcat` in both shells by hitting `^C`

