#! /usr/bin/env bash
wget https://storage.googleapis.com/jsingh-bigdata-public/inaugs.tar.gz
hadoop fs -mkdir /user/inputs/
hadoop fs -put -f inaugs.tar.gz  /user/inputs/
hadoop jar /usr/lib/hadoop/hadoop-streaming.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input /user/inputs/inaugs.tar.gz -output /user/j_singh/inaugs
