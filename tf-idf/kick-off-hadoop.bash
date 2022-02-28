#! /usr/bin/env bash
#
# copy-paste these lines into the hadoop master shell
#
hadoop fs -mkdir /user/inputs/
hadoop fs -mkdir /user/inputs/abc
wget https://storage.googleapis.com/jsingh-bigdata-public/abc.zip
unzip abc.zip -d abc
hadoop fs -put -f abc/* /user/inputs/abc
hadoop jar /usr/lib/hadoop/hadoop-streaming.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -numReduceTasks 1 -input /user/inputs/abc -output /user/j_singh/count_abc

