#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# !pip install pandas

# Historical Daily Prices
# !pip install finance-datareader

import pandas as pd
import time, datetime, sys
import os, pathlib

import FinanceDataReader as fdr

tech_df = fdr.DataReader('GOOG, MSFT', '2020')
# print(tech_df)

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
# print (sys.path, file=sys.stderr)

dates = tech_df.index.rename('Date')
init_date = list(dates)[0]
last_hist_date = list(dates)[-1]

init_delay_seconds = 30
interval = 5

scaler = tech_df['GOOG'][init_date]/tech_df['MSFT'][init_date]
goog  = tech_df['GOOG']
msft  = tech_df['MSFT']
tech_df['scaledMSFT'] = msft*scaler
print (tech_df[0:3])

print ('Sending daily GOOG and MSFT prices from %10s to %10s ...' % (str(init_date)[:10], str(last_hist_date)[:10]), flush=True, file=sys.stderr)
print ("... each day's data sent every %d seconds ..." % (interval), flush=True, file=sys.stderr)
print ('... beginning in %02d seconds ...' % (init_delay_seconds), flush=True, file=sys.stderr)
print ("... MSFT prices adjusted to match GOOG prices on %10s ..."  % (init_date), flush=True, file=sys.stderr)

from tqdm import tqdm
for left in tqdm(range(init_delay_seconds)):
    time.sleep(0.5)

for date in list(dates):       
    print ('%10s\t%.4f\t%.4f' % (str(date)[:10], tech_df['GOOG'][date], tech_df['scaledMSFT'][date]))
    time.sleep(float(interval))

exit(0)

# Real Time Prices
# !pip install yahoo_fin
from yahoo_fin import stock_info

for t in range(10):
    now = datetime.datetime.now()
    goog_price = stock_info.get_live_price('GOOG')
    msft_price_adj = stock_info.get_live_price('MSFT') * scaler
    print ('%10s\t%.4f\t%.4f' % (str(now)[:19], goog_price, msft_price_adj))
    time.sleep(5.0)

exit(0)
