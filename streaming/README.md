# Streaming Functions

## Netcat pipes

Open two terminals on the same machine. One will be the sender terminal, the other will be the receiver terminal.

Into the receiver terminal, type

    nc -lk 9999

The receiver is now ready to receive a data stream on port 9999. 

Into the sender terminal, type

    cat | nc localhost 9999

The sender is now set up to send a data stream on port 9999. After this, anything you type into the sender terminal will be echoed on the receiver terminal.

This is a good time to try the next step: run word-count in pyspark, listening on port 9999. Now if you type something into the sender terminal, it will make its way to spark streaming.

## DJ-30
To simulate a data stream, you are given a python program dj30-feeder.py which reads in dj30.csv file and pipes it, line by line. dj30.csv contains a 25-year history of the Dow Jones Industrial Average prices. 

We will be using the netcat utility (nc) to pipe a stream into Spark. The syntax is

    ./dj30-feeder.py  | nc localhost 9999

If you would like to see the data as they are being pushed into the pipe, you may use

    ./dj30-feeder.py  | tee /dev/stderr | nc localhost 9999 

Get the streaming functions and bring them into the master machine of your spark cluster.

## News feed
Similarly, run `news-feeder.py | nc localhost 9999` to feed the news into a pyspark DStream.

    ./news-feeder.py  | tee /dev/stderr | nc localhost 9999