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

    calculateTFIDF(wcss)

def calculateTFIDF(wcss):
    expected = '''
    fnam1
        word1 tfidf1
        word2 tfidf2
        word3 tfidf3
          ::
        wordn tfidfn
    '''

    print (wcss)
    wordset = collections.Counter()
    for fnam in wcss:
        wordset.update(wcss[fnam])
    wordset = list(wordset.keys())

    def calculateTF(wordset, wcss):
        def calcTF(bow):
            counter =  dict(collections.Counter(bow))
            return dict(collections.Counter(bow))

        def recalcTF(wordset, wc):
            tf = dict.fromkeys(wordset,0)
            counter = collections.Counter(wc)
            total = sum(counter.values())
            for w in wc:
                tf[w]=counter[w]/total
            return tf

        for fnam in wcss:
            wc = calcTF(wcss[fnam])
            tf = recalcTF(wordset, wc)
            # print ('wc', 'tf', wc, tf)
            ret = {fnam:recalcTF(wordset, wcss[fnam]) for fnam in wcss}
        return ret

    def calculateIDF(wordset, wcss):
        # pp.pprint(wcss)
        wcs = [wcss[fnam] for fnam in wcss]
        d_bow = {'wc_{}'.format(i):list(set(b)) for i,b in enumerate(wcs)}
        N=len(d_bow.keys())
        l_bow = []
        for b in d_bow.values():
            l_bow+=b
            # print ('l_bow', l_bow)
            counter = dict(collections.Counter(l_bow))
            # print ('counter', counter)
            idf_diz = dict.fromkeys(wordset,0)
            # print ('idf_diz', idf_diz)
            for w in wordset:
                try:
                    ctr = counter[w]
                except KeyError:
                    ctr = 0
                idf_diz[w] = np.log((1+N)/(1+ctr))+1
            return idf_diz

    idf = calculateIDF(wordset, wcss)

    # Calculate TF values
    tf =  calculateTF(wordset, wcss)
    print('TFs', tf)

    # Calculate TF.IDF values
    tfidfs = {}
    for fnam in wcss:
        tfidfs[fnam] = {}
        for w in wordset:
            tfidfs[fnam][w] = tf[fnam][w]*idf[w]
    print(tfidfs)

    # Output the TF.IDF values
    for fnam in sorted(wcss):
        print ('\n\n', fnam)
        sorted_tfidf = dict( sorted(tfidfs[fnam].items(), key = lambda item: item[1], reverse = True))
        for w in sorted_tfidf:
            if sorted_tfidf[w] > 0.0:
                print (w, sorted_tfidf[w])

    return None


if __name__ == "__main__":
    main(sys.argv)
