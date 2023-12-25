#!/usr/bin/env python

import sys
import os
import re, string
import collections

import requests
stopwords_list = requests.get("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
stopwords = set(stopwords_list.decode().splitlines()) 
stopwords = list(stopwords)

def main(argv):
    line = sys.stdin.readline()
    remove_chars = set(string.punctuation)
    pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
    try:
        while line:
            if "map_input_file" in os.environ:
                filename = os.environ["map_input_file"]
                phrase = line
            else:
                filename = line.split('|')[0]
                phrase = line.split('|')[1]
            # remove leading and trailing whitespace
            phrase = phrase.strip()
            exclude = set(string.punctuation)
            phrase = ''.join(ch for ch in phrase if ch not in exclude)
            # Remove non-ascii characters. https://stackoverflow.com/a/20078869/653651
            phrase = re.sub(r'[^\x00-\x7F]+',' ', phrase)
            # split the phrase into words
            words = [word.lower() for word in phrase.split()]
            mapout(filename, words)

            line = sys.stdin.readline()
    except EOFError as error:
        return None

def mapout(filename, words):
    list_ = [itm for itm in words if itm not in stopwords]
    wcs =  dict(collections.Counter(list_))
    for word in wcs:
        print ('mapout:\t%s\t%s\t%s' % (word, filename, str(wcs[word])))

if __name__ == "__main__":
    main(sys.argv)

