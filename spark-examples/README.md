# Spark Structured Streaming Demo

This demo can be run in a Dataproc cluster ***or*** on the Halligan servers at Tufts.

## Steps:

1. Log into master machine of the cluster (or open a terminal into a Halligan server).
2. Git clone my repo: `git clone https://github.com/singhj/big-data-repo.git`
3. Install `tqdm`: `sudo apt install python3-tqdm`. `sudo` is disallowed on the Halligan servers. Instead, use `pip3 install tqdm`.
4. Install `nltk`: `sudo apt install python3-nltk`. `sudo` is disallowed on the Halligan servers. Instead, use `pip3 install nltk`.
5. Set the `PATH` environment variable: `PATH="$PATH:$HOME/big-data-repo/:$HOME/big-data-repo/spark-examples/"`
6. Test `netcat`:
    * Start a second (listener) shell. (Or open a second terminal window into the Halligan server to do this).
    * In the first (sender shell), set up sender: `nc -lk 9999`
    * In the listener shell, `nc localhost 9999`
    * Any words typed into the sender shell should appear in the listener shell.
    * Stop `netcat` in both shells by hitting `^C`
7. Set up `netcat` pipeline for inaugural speeches:
    * In the sender shell, ``inaugural-speech-feeder.py | nc -lk 9999``. You have about 30 seconds to start the listener (the next step).
    * In the listener shell, ``nc localhost 9999``
    * If it worked, you should see the inaugural speeches appear in the listener.
    * Stop `netcat` in both shells by hitting `^C`
8. Set up wordcount pipeline:
    * In the sender shell, ``inaugural-speech-feeder.py | nc -lk 9999``. You have about 30 seconds to start the listener (the next step).
    * In the listener shell, ``spark-submit `which structured-network-wordcount.py` localhost 9999``
    * If it worked, you should see wordcounts for the inaugural speeches appear in the listener.
    * Stop `netcat` in both shells by hitting `^C`
