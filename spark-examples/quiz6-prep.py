#!/usr/bin/env python3

import os
os.system('sudo apt-get install python3-pip')

try:
    import nltk
except ImportError:
    print ('nltk is not installed')
    os.system('pip3 install nltk')
finally:
    pass

try:
    import nltk
except AttributeError:
    print ("AttibuteError")
    os.system('sudo sed -i', 's/regex.Pattern:/\"regex.Pattern\":/g','/opt/conda/default/lib/python3.8/site-packages/nltk/tokenize/casual.py')
finally:
    pass
