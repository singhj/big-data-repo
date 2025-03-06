#!/usr/bin/env python3
import time, datetime
import pandas as pd
import json

import re
import sys, os
dir_path = os.path.realpath(__file__)

prices_df = pd.read_csv(os.path.dirname(dir_path) + '/../datasets/aapl.csv')
prices_df.dropna(inplace=True)
# print (prices_df.columns) # 'Date', 'Close/Last', 'Volume', 'Open', 'High', 'Low'

# Convert DataFrame rows to a list of dictionaries
records = prices_df.to_dict(orient='records')

price = lambda s: float(s.replace(" ", "").replace("$", ""))
date  = lambda s: datetime.datetime.strptime(s, "%m/%d/%Y").isoformat()

date_string = "10/25/2022"
date_format = "%m/%d/%Y"

datetime_object = datetime.datetime.strptime(date_string, date_format)

for record in records:
    record['Date'] = date(record['Date'])
    record['Close/Last'] = price(record['Close/Last'])
    record['Open'] = price(record['Open'])
    record['High'] = price(record['High'])
    record['Low'] = price(record['Low'])

    print (json.dumps(record), flush=True)
    time.sleep(0.5)
    
