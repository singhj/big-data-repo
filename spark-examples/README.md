# Spark Structured Streaming Demo

## Prerequisites:

1. Create a Dataproc cluster and log into its master machine. This code also runs on the Halligan servers at Tufts.
2. Git clone my repo: `git clone https://github.com/singhj/big-data-repo.git`
3. Install `tqdm`: `sudo apt install python3-tqdm`. `sudo` is disallowed on the Halligan servers. Instead, use `pip3 install tqdm`.
4. Install `nltk`: `sudo apt install python3-nltk`. `sudo` is disallowed on the Halligan servers. Instead, use `pip3 install nltk`.
5. Test `netcat`:
    * (this is the sender shell). `cd ~/big-data-repo/spark-examples`
    * Start a second (listener) shell, also `cd ~/big-data-repo/spark-examples` there. (Open a second terminal window into the Halligan server to do this).
    * In the sender shell, set up sender: `nc -lk 9999`
    * In the listener shell, `nc localhost 9999`
    * Any words typed into the sender shell should appear in the listener shell.
    * Stop `netcat` in both shells by hitting `^C`
6. Set up `netcat` pipeline for inaugural speeches:
    * In the sender shell, `inaugural-speech-feeder.py | nc -lk 9999`. You have about 30 seconds to start the listener (the next step).
    * In the listener shell, `nc localhost 9999`
    * If it worked, you should see the inaugural speeches appear in the listener.`
    * Stop `netcat` in both shells by hitting `^C`
7. Set up wordcount pipeline:
    * In the sender shell, `inaugural-speech-feeder.py | nc -lk 9999`. You have about 30 seconds to start the listener (the next step).
    * In the listener shell, `spark-submit structured-network-wordcount.py localhost 9999`
    * If it worked, you should see wordcounts for the inaugural speeches appear in the listener.`
    * Stop `netcat` in both shells by hitting `^C`

