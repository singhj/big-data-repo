#!/usr/bin/env python

import nltk
import nltk.corpus
from nltk.corpus import inaugural
nltk.download('inaugural')

REPLACEMENTS = [
    (". ",   ".\n"),     # Add a newline after periods, to improve readability.
    ("Mr.\n", "Mr. "),    # Don't treat Mr. as end of sentence.
    ("Ms.\n", "Ms. "),    # Don't treat Mr. as end of sentence.
    ("Mrs.\n", "Mrs. "),  # Don't treat Mrs. as end of sentence.
]

speech_names = nltk.corpus.inaugural.fileids()[-10:]
for name in speech_names:
    text = inaugural.raw(name)
    # Replace all non-ascii characters with spaces
    text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    # Replace multiple spaces with a single space
    text = ' '.join(text.split())
    
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)

    with open('inaug_'+ name, 'w') as writer:
        writer.writelines(text+'\n')


