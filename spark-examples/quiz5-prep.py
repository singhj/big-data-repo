#!/usr/bin/env python3

import os, sys
import traceback as tb

# install pip if necessary
os.system('sudo apt-get -y install python3-pip')

try:
    import nltk
except ImportError:
    print ('nltk was not installed, installing...')
    os.system('pip3 install nltk')
except AttributeError as exception:
    exception_type, exception_object, exception_traceback = sys.exc_info()
    foo = tb.extract_tb(exception_traceback)[-1]
    print ('Repairing file', foo.filename)
    filename = foo.filename

    # This repair: https://github.com/nltk/nltk/commit/6428c9288a86658cb3d9a1e91816c4bcf162a6f0
    os.system(' '.join(['sudo sed -i',
                        's/regex.Pattern:/\\"regex.Pattern\\":/g',
                        filename]))

finally:
    pass


