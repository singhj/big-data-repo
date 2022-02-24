wget https://storage.googleapis.com/jsingh-bigdata-public/inaugs.tar.gz
hadoop fs -put /user/inputs/inaugs.tar.gz
hadoop jar /usr/lib/hadoop/hadoop-streaming.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input /user/inputs/inaugs.tar.gz -output /user/j_singh/inaugs
