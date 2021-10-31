#!/usr/bin/env python3
import sys
import time, datetime
import pandas as pd
import random

class Click:
    senders = []
    urls = []
    delay = tuple()
    def __init__(self, senders, urls, delay_mu, delay_sigma):
        self.senders = senders
        self.urls  = urls
        self.delay = (delay_mu, delay_sigma,)
    def __str__(self):
        return '%s: %s (%f.3, %f.3)' % (self.senders, self.urls, self.delay[0], self.delay[1])
    def get(self):
        while True:
            delta_t = random.normalvariate(self.delay[0], self.delay[1])
            while delta_t <= 0.0:
                delta_t = random.normalvariate(self.delay[0], self.delay[1])
            time.sleep(delta_t)
            ret = (datetime.datetime.now().time(), random.choice(self.senders), random.choice(self.urls))
            yield ret


clickgen = Click(('Alice', 'Bob', 'Cass'), ('url1', 'url2', 'url3'), 4.0, 1.0)

clicks = 5
for click in clickgen.get():
    clicks -= 1
    print (clicks, click, flush = True)
    if clicks <= 0:
        break

