#!/usr/bin/env python3
import nltk
import random
import time

nltk.download('inaugural')
nltk.download('punkt')
from nltk.corpus import inaugural
fileids = nltk.corpus.inaugural.fileids()
# print (fileids, flush=True)

def next_delay(self):
    return random.normalvariate(self.delay[0], self.delay[1])

for fileid in fileids:
    sents = inaugural.sents(fileid)
    for sent in sents:
        print (fileid, sent, flush=True)
        minutes = 150
        words = len(sent)
        delay = 60.0 * words/150
        # print (delay, words, words/delay, flush=True)
        time.sleep(delay)
    # break
