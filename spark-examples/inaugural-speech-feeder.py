#!/usr/bin/env python3
import sys
import nltk
import random
import time
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
print (sys.path)

import clean_text

nltk.download('inaugural')
nltk.download('punkt')
from nltk.corpus import inaugural
fileids = nltk.corpus.inaugural.fileids()
# print (fileids, flush=True)

def random_delay(avg):
    return random.normalvariate(float(avg), 0.15*float(avg))

for fileid in fileids:
    sents = inaugural.sents(fileid)
    for sent in sents:
        print ('sent', ' '.join(sent))
        rate = 150/60
        words = len(sent)
        delay = random_delay(words/rate)
        print (fileid, f"{delay:5.2f}", ' '.join(sent), flush=True, file=sys.stderr)
        print (fileid, (clean_text.clean(' '.join(sent))), flush=True)
        # print (delay, words, words/delay, flush=True)
        time.sleep(delay)
    # break
