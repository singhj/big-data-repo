#!/usr/bin/env python
import re

def clean_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub('[\d\n]', ' ', text)
    text = ' '.join([w for w in text.split() if len(w)>3])
    return text.strip()
