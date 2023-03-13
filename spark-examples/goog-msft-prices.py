#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
!pip install market-prices
!pip install pandas
"""
import time, datetime, sys
import os


"""
Stock Quotes -- Mar 12 2023
"""





# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
from market_prices import PricesYahoo


"""
# importing matplotlib module
import matplotlib.pyplot as plt
plt.style.use('default')
  
# %matplotlib inline
"""
prices = PricesYahoo("MSFT, GOOG") # prices for Microsoft, Google
prices_l2 = prices.get("1D", start="2020-03-10")
prices_l2.index.strftime('%Y-%m-%d')
# uncomment next line for understanding what it does
# prices_l2.columns

prices_l2

prices_l1 = prices_l2.copy()
prices_l1.columns = prices_l1.columns.get_level_values(0)
# uncomment next line for understanding what it does
# prices_l1

# uncomment next line for understanding what it does
# prices_l2[('GOOG','close')]

# uncomment next line for understanding what it does
# prices_l2[('MSFT', 'close')]

prices_l2_v2 = prices_l2.copy()
prices_l2_v2.index.rename('Date')

closes_v1 = pd.concat([prices_l2_v2[('GOOG','close')],prices_l2_v2[('MSFT', 'close')]],axis=1)
closes_v1.columns = ["".join(a) for a in closes_v1.columns.to_flat_index()]
closes_v1

closes_v2 = closes_v1.copy()
scaler = closes_v2['GOOGclose']['2020-03-10']/closes_v2['MSFTclose']['2020-03-10']
closes_v2['MSFT-comp'] = closes_v2['MSFTclose']*scaler
closes_v2

goog_msft_df = closes_v2.copy()
goog_msft_df['Date'] = goog_msft_df.index
goog_msft_df

iters = 750
for _, row in goog_msft_df.iterrows():
    print(row['Date'].date(), row['GOOGclose'], row['MSFT-comp'], flush = True)
    time.sleep(1.0)
    iters -= 1
    if iters == 0:
        break

"""
plt.figure(figsize=(10, 6), dpi=100)
closes_v2['GOOGclose'].plot(label='Google', color='blue')
closes_v2['MSFTclose'].plot(label='Microsoft', color='pink')
closes_v2['MSFT-comp'].plot(label='Microsoft', color='red')
"""
