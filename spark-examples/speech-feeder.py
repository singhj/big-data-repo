#!/usr/bin/env python3
import sys
import nltk
import random
import time
import pathlib

# Outputs cleaned up text at a normal typing rate. 
# Outputs a copious amount of information to stderr.

# Example Usage: To view the output:
    # spark-examples/inaugural-speech-feeder.py 2>/dev/null

# Example Usage: To send the output using nc:
    # spark-examples/inaugural-speech-feeder.py 2>/dev/null | nc localhost 9999

# Example Usage: To view the output while also sending using nc:
    # For grabbing in the shell:
         # spark-examples/inaugural-speech-feeder.py 2>/dev/null | tee | nc localhost 9999
    # For sending to spark-submit for wordcounts:
         # spark-examples/inaugural-speech-feeder.py 2>/dev/null | tee | nc -lk 9999


sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
print (sys.path, file=sys.stderr)

import clean_text

nltk.download('inaugural')
nltk.download('punkt')
from nltk.corpus import inaugural
fileids = nltk.corpus.inaugural.fileids()

def random_delay(avg):
    return random.normalvariate(float(avg), 0.15*float(avg))

for fileid in fileids:
    # Sentences
    sents = inaugural.sents(fileid)
    print (fileid, '#### #### ####', flush=True, file=sys.stderr)
    for sent in sents:

        rate = 150/60
        words = len(sent)
        delay = random_delay(words/rate)

        print (fileid, '|', clean_text.clean(' '.join(sent)), flush=True)
        time.sleep(delay)
    # break
