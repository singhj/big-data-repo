#!/usr/bin/env python
"""reducer.py"""

# python mapper.py < input.txt | sort | python reducer.py
# hadoop jar /usr/lib/hadoop/hadoop-streaming.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input /user/inputs/inaugs.tar.gz -output /user/j_singh/inaugs

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
        _, word, fnam, count = line_.split('\t', 3)

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

    tfidf = calculateTFIDF(wcss) # Implement this function

def calculateTFIDF(wcss):
    expected = '''
    fnam1
        word1 tfidf1
        word2 tfidf2
        word3 tfidf3
          ::
        wordn tfidfn
    '''
    
    for fnam in sorted(wcss):
        wcs = wcss[fnam]
        print ('\n\n', fnam)
        sorted_wcs = dict( sorted(wcs.items(), key = lambda item: item[1], reverse = True))
        for w in sorted_wcs:
            print (w, sorted_wcs[w])
    return None

if __name__ == "__main__":
    main(sys.argv)
