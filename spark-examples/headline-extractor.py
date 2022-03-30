#!/usr/bin/env python3
import time, datetime
import pandas as pd

import re
import sys, os
dir_path = os.path.realpath(__file__)

def pre_process(text):
    # lowercase
    text=text.lower()
    # remove tags
    text=re.sub("","",text)
    # remove numbers and dollar amounts
    text = re.sub(r'[0-9\,$]+', '', text)
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    # remove short words
    text = ' '.join([word for word in text.split() if len(word) > 3])
    return text

def tolist(text):
    return text.split()

# Extracted from: https://www.nature.com/articles/s41599-020-0523-3#Sec7 [Supplementary information]
hdlines_df = pd.read_csv(os.path.dirname(dir_path) + '/data/2020-headlines.csv')
hdlines_df.dropna(inplace=True)
hdlines_df.drop(columns=['SNO', 'Website'], inplace=True)
hdlines_df

hdlines_df['text'] = hdlines_df['News']
hdlines_df['text'] = hdlines_df['text'].apply(lambda x:pre_process(x))
hdlines_df['text']
hdlines = hdlines_df['text']
hdlines

from collections import defaultdict

wordsFreq = defaultdict(int)
lines = hdlines.tolist()
for line in lines:
    words = line.split()
    for word in words:
        if len(word) > 3:
            wordsFreq[word] += 1


def topn(wordsFreq, n):
    return sorted(wordsFreq.items(), key=lambda k_v: k_v[1], reverse=True)[:n]

understood_words = set([word for word in wordsFreq.keys() if wordsFreq[word] > 1])
print ('collected %d-word newsworthy vocabulary' % len(understood_words), file=sys.stderr)

filename = os.path.dirname(dir_path) + '/data/headline_words.txt'
with open(filename, 'a') as the_file:
    for word in understood_words:
        the_file.write(word+'\n')

print ('wrote newsworthy vocabulary into %s' % filename, file=sys.stderr)

