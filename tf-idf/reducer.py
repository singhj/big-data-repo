#!/usr/bin/env python
"""reducer.py"""

# python mapper.py < input.txt | sort | python reducer.py

import collections
from operator import itemgetter
import sys
import numpy as np
import pprint
pp = pprint.PrettyPrinter(indent = 4, width = 80)

def main(argv):
    current_word = None
    current_fnam = None
    current_count = 0
    word = None
    wcss = {}

    # input comes from STDIN
    for line in sys.stdin:
        # remove leading and trailing whitespace
        line_ = line.strip()

        # parse the input we got from mapper.py
        mapkey, count = line_.split('\t', 1)
        mapkey = mapkey.replace('mapout: ','')

        word, fnam = mapkey.split('|')
        # convert count (currently a string) to int
        try:
            count = int(count)
            if fnam in wcss:
                wcss[fnam].update({word:count})
            else:
                wcss[fnam] = collections.Counter()
                wcss[fnam].update({word:count})

        except ValueError:
            # count was not a number, so silently
            # ignore/discard this line
            pass

    for fnam in wcss:
        wcs = dict(wcss[fnam])
        print (fnam)
        sorted_words = dict(sorted(wcs.items(), key=lambda x: x[1], reverse=True))
        for w in sorted_words:
            print (w, sorted_words[w])

if __name__ == "__main__":
    main(sys.argv)
