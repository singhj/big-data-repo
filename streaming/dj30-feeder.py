#!/usr/bin/env python3
import time, datetime, sys
import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# Extracted from: https://www.nature.com/articles/s41599-020-0523-3#Sec7 [Supplementary information]
dj30_df = pd.read_csv(os.path.dirname(dir_path) + '/data/dj30.csv')
dj30_df.dropna(inplace=True)
dj30_df = dj30_df.loc[:,['Date', 'Close']]
dj30 = dj30_df['Close'].tolist()

class CloseFeed:
    source = None
    def __init__(self, source):
        self.source = source

    def getClose(self):
        i = 0
        while True:
            time.sleep(0.25)
            i += 1
            yield self.source[i-1]

dj30CloseFeed = CloseFeed(dj30)

for close in dj30CloseFeed.getClose():
    print (close, flush = True)
