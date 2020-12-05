# Streaming Problems

## Netcat pipes

Open two terminals on the same machine. One will be the sender terminal, the other will be the receiver terminal.

Into the receiver terminal, type

    nc -lk 9999

The receiver is now ready to receive a data stream on port 9999. 

Into the sender terminal, type

    cat | nc localhost 9999

The sender is now set up to send a data stream on port 9999. After this, anything you type into the sender terminal will be echoed on the receiver terminal.

This is a good time to try the next step: run word-count in pyspark, listening on port 9999. This will confirm that your environment is established and is working correctly. If you type something into the sender terminal, it will make its way to spark streaming.

## Installing Dependencies

Please install `pip3`, `pandas` and `feedparser` on the master of your cluster:

    sudo apt-get install python3-pip
    pip3 install pandas
    pip3 install feedparser

Also `git clone` this repo with

    git clone https://github.com/singhj/big-data-repo

## DJ-30
To simulate a data stream, you are given a python program dj30-feeder.py which reads in dj30.csv file and pipes it, line by line. dj30.csv contains a 25-year history of the Dow Jones Industrial Average prices. 

We will be using the netcat utility (nc) to pipe a stream into Spark. The syntax is

    ./big-data-repo/streaming/dj30-feeder.py  | nc -lk 9999

If you would like to see the data in the sender terminal (in addition to the receiver terminal) as they are being pushed into the pipe, you may use

    ./big-data-repo/streaming/dj30-feeder.py  | tee /dev/stderr | nc -lk 9999 


## News feed

Similarly, run `./big-data-repo/news-feeder.py | nc -lk 9999` to feed the news into a pyspark DStream. Or, if you prefer,

    ./big-data-repo/streaming/news-feeder.py  | tee /dev/stderr | nc -lk 9999

## In PySpark

The code below does wordcount in PySpark. You will have to adapt it to the quiz exercises.

    sc.stop()
    from pyspark import SparkContext
    from pyspark.streaming import StreamingContext

    sc = SparkContext("local[2]", "NetworkWordCount")
    ssc = StreamingContext(sc, 4)
    lines = ssc.socketTextStream("localhost", 9999)
    words = lines.flatMap(lambda line: line.split(" "))
    pairs = words.map(lambda word: (word, 1))
    wordCounts = pairs.reduceByKey(lambda x, y: x + y)
    wordCounts.pprint()

    ssc.start()
    ssc.awaitTermination()

