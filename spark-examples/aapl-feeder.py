#!/usr/bin/env python3

import time, datetime, sys
import pandas as pd
import os

dir_path = os.path.realpath(__file__)

aapl_df = pd.read_csv(os.path.dirname(dir_path) + '/../datasets/aapl.csv')
aapl_df.dropna(inplace=True)
aapl_df = aapl_df.loc[:,['Date', 'Close/Last']]
aapl_df = aapl_df.iloc[::-1]

for _, row in aapl_df.iterrows():
    print(row['Date'], row['Close/Last'], flush = True)
    time.sleep(1.0)

