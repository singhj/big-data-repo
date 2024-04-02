#!/usr/bin/env python3
import sys, tqdm
import nltk
import random
import time
import pathlib

import pandas as pd, numpy as np

afinn_src = 'https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt'

afinn_df = pd.read_csv(afinn_src, sep='\t', header=None, dtype={'word': str, 'valence': np.int32})
afinn_df = afinn_df.set_axis(['word', 'valence'], axis=1)
afinn_df.set_index('word', inplace=True)
afinn_dict = afinn_df.to_dict('dict')['valence']
afinn_words = list(afinn_dict.keys())

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
# print (sys.path, file=sys.stderr)

init_delay_seconds = 30
from tqdm import tqdm
for left in tqdm(range(init_delay_seconds)):
    time.sleep(0.5)

deltaT = 2.0
def random_delay(avg):
    return random.normalvariate(float(avg), 0.15*float(avg))

random.seed (951)
words = []
sent = 0
for i in range(1000):
    indx = random.randint(0,5000)
    if indx < 3382:
        words.append(afinn_words[indx])
        # print(afinn_words[indx])
    else:
        if len(words) < 3:
            continue
        else:
            print (' '.join(words), flush=True)
            time.sleep(random_delay(deltaT))
            sent += 1
            words = []

print ('Sent', sent, 'utterings', flush=True, file=sys.stderr)
