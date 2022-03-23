#!/usr/bin/env python3

import os, sys
import subprocess
import traceback as tb
os.system('sudo apt-get -y install python3-pip')

try:
    import nltk
except ImportError:
    print ('nltk is not installed')
    os.system('pip3 install nltk')
except AttributeError as exception:
    # tb.print_stack()
    # print ("AttibuteError")
    exception_type, exception_object, exception_traceback = sys.exc_info()
    foo = tb.extract_tb(exception_traceback)[-1]
    print ('filename', foo.filename)
    filename = foo.filename
    print('******', filename)
    os.system(' '.join(['sudo sed -i',
                        's/regex.Pattern:/\\"regex.Pattern\\":/g',
                        filename]))

finally:
    pass


