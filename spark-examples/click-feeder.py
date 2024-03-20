#!/usr/bin/env python3

import importlib
clickgen = importlib.import_module("click-gen")

from clickgen import *
max_evs = 60           # Total number of events that will be generated. 
                       # If you want to make it run forever, set this number to like a million

n_senders = 6         # Number of senders
n_queries = 6000      # How many different queries (or messages a sender can send)

dispatcher = Dispatcher()
sender_names = shuffle(['sndr%04d' % i for i in range(n_senders)])
senders = [dispatcher.add_sender(Sender(sender_name, n_queries, 1.5, 0.5)) for sender_name in sender_names]

for ev in dispatcher.launch():
    print(ev, flush=True)
    max_evs -= 1
    if max_evs == 0:
        break


