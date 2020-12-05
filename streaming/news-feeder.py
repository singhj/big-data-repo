#!/usr/bin/env python3
import sys
import feedparser, time, datetime
import pandas as pd

class Feed:
    name = ''
    url = None
    max_delay = None
    def __init__(self, name, url, max_delay):
        self.name = name
        self.url  = url
        self.max_delay = max_delay

    def __str__(self):
        return '%s: %s' % (self.name, self.url)

    def getHeadline(self):
        d = feedparser.parse (self.url)
        for post in d.entries:
            time.sleep(0.25)
            ret = (datetime.datetime.now().time(), self.name, post.title, post.link)
            yield ret

#

feeds = (
    Feed('nyt-home', 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 1),
    Feed('nyt-sun', 'https://rss.nytimes.com/services/xml/rss/nyt/sunday-review.xml', 1),
    Feed('nyt-hlth', 'https://rss.nytimes.com/services/xml/rss/nyt/Health.xml', 1),
    Feed('nyt-wrld', 'https://www.nytimes.com/section/world/rss.xml', 1),
    Feed('nyt-bsns', 'http://feeds.nytimes.com/nyt/rss/Business', 1),
    Feed('nyt-tech', 'http://feeds.nytimes.com/nyt/rss/Technology', 1),
    Feed('nyt-sprt', 'https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml', 1),
    Feed('nyt-scnc', 'http://www.nytimes.com/services/xml/rss/nyt/Science.xml', 1),
    Feed('nyt-arts', 'https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml', 1),
    Feed('nyt-trvl', 'https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml', 1),
    Feed('nyt-usa',  'http://www.nytimes.com/services/xml/rss/nyt/US.xml', 1),
    Feed('bbc-hlth', 'http://feeds.bbci.co.uk/news/health/rss.xml', 1),
    Feed('bbc-brkn', 'https://bbcbreakingnews.com/feed', 1),
    Feed('bbc-bsns', 'http://feeds.bbci.co.uk/news/business/rss.xml', 1),
    Feed('bbc-pltc', 'http://feeds.bbci.co.uk/news/politics/rss.xml', 1),
    Feed('bbc-educ', 'http://feeds.bbci.co.uk/news/education/rss.xml', 1),
    Feed('bbc-scnc', 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml', 1),
    Feed('bbc-tech', 'http://feeds.bbci.co.uk/news/technology/rss.xml', 1),
    Feed('bbc-arts', 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml', 1),
)

'''
# Used for testing, now commented out
titles = []
for feed in feeds:
    for (tt, name, title, link) in feed.getHeadline():
        words = pre_process(title).split()

        if all([x in understood_words for x in words]):
            # print('i know this: ', title)
            pass
        else:
            print(title)
'''

titles = []
for feed in feeds:
    for (tt, name, title, link) in feed.getHeadline():
        print (title, flush = True)

