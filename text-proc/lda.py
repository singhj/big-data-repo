import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[1]") \
                    .appName('Reviews LDA') \
                    .getOrCreate()

sc = spark.sparkContext

from pyspark.sql.types import *

#
# To prepare the environment and the data:
#     git config --global user.email "j.singh@datathinks.org"
#     git config --global user.name "singhj"
#
# sudo sed -i 's/regex.Pattern:/\"regex.Pattern\":/g' /opt/conda/default/lib/python3.8/site-packages/nltk/tokenize/casual.py
# ~/big-data/text-proc/reviews_setup.sh
#

# To run LDA:
test = '''
from lda import spark, sc, retrieve, tokenize, tfidf, lda_train, model_show

# Load the data from HDFS into a Spark DataFrame
data = retrieve(sc)
data.printSchema()

tokens = tokenize(data)
result_tfidf = tfidf(sc, tokens)

# Train the model
model = lda_train(result_tfidf)

# Inspect the results
topics_mapped = model_show(tokens, model)

'''
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

import pandas as pd
import pyspark
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[1]") \
                    .appName('Reviews LDA') \
                    .getOrCreate()
sc = spark.sparkContext

from pyspark.sql.types import *


def retrieve(sc):
    import os    
    data = spark.read.format("csv") \
          .options(header='true', inferschema='true') \
          .load(os.path.realpath("/user/j_singh/reviews.csv"))

    return data

def tokenize(data):
    import re
    from nltk.corpus import stopwords
    reviews = data.rdd.map(lambda x : x['Review Text']).filter(lambda x: x is not None)
    StopWords = stopwords.words("english")
    tokens = reviews                                                   \
        .map( lambda document: document.strip().lower())               \
        .map( lambda document: re.split(" ", document))          \
        .map( lambda word: [x for x in word if x.isalpha()])           \
        .map( lambda word: [x for x in word if len(x) > 3] )           \
        .map( lambda word: [x for x in word if x not in StopWords])    \
        .zipWithIndex()
    return tokens

def tfidf(sc, tokens):
    from pyspark.sql import SQLContext
    from pyspark.ml.feature import CountVectorizer , IDF
    sqlContext = SQLContext(sc)
    df_txts = sqlContext.createDataFrame(tokens, ["list_of_words",'index'])
    #
    # TF
    #
    cv = CountVectorizer(inputCol="list_of_words", outputCol="raw_features", vocabSize=5000, minDF=10.0)
    cvmodel = cv.fit(df_txts)
    result_cv = cvmodel.transform(df_txts)
    #
    # IDF
    #
    idf = IDF(inputCol="raw_features", outputCol="features")
    idfModel = idf.fit(result_cv)
    result = idfModel.transform(result_cv)
    #
    return result

def lda_train(result_tfidf):
    from pyspark.ml.linalg import Vectors, SparseVector
    from pyspark.ml.clustering import LDA
    #
    lda = LDA(k=10, seed=1, optimizer="em")
    lda.setMaxIter(100)
    #
    model = lda.fit(result_tfidf[['index', 'features']])
    # model = LDA.train(result_tfidf[['index', 'features']].rdd.map(list), k=num_topics, maxIterations=max_iterations)
    return model

def model_show(tokens, model):
    from pyspark.ml.feature import CountVectorizer
    from pyspark.sql.functions import udf
    from pyspark.sql.types import ArrayType

    df_txts = sqlContext.createDataFrame(tokens, ["list_of_words",'index'])
    cv = CountVectorizer(inputCol="list_of_words", outputCol="wrd_index", vocabSize=2000)
    cvmodel = cv.fit(df_txts)
    vocab = cvmodel.vocabulary  
    topics = model.describeTopics()
    vocab_broadcast = sc.broadcast(vocab)
    def map_termID_to_Word(termIndices):
        words = []
        for termID in termIndices:
            words.append(vocab_broadcast.value[termID])
        return words

    udf_map_termID_to_Word = udf(map_termID_to_Word , ArrayType(StringType()))
    topics_mapped = topics.withColumn("topic_desc", udf_map_termID_to_Word(topics.termIndices))
    return topics_mapped
