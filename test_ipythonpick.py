# -*- coding: utf-8 -*-

# mock module dependencies
import sys
sys.modules['sublime'] = __import__('stub_sublime')
sys.modules['sublime_plugin'] = __import__('stub_sublime_plugin')

import StringIO
from pytest import mark

from ipythonpick import get_sentences  # noqa

# contents taken from an actual ipython_log.py files (with ipython==3.2.0)
contents_and_sentences = [
    ('''# IPython log file


def f(a, b):
    return a, b

f(1,2)
f(2,3)
def f(a, b):
    return a, b, 34

range(9)
if True:
    print 23

for x in [1,2]:
    print x

42
42
for x in [1,2]:
    print x
if 2 > 1:
    print 21

34
''',  # -----------------------------------------
     '''
def f(a, b):
    return a, b

f(1,2)

f(2,3)

def f(a, b):
    return a, b, 34

range(9)

if True:
    print 23

for x in [1,2]:
    print x

42

42

for x in [1,2]:
    print x

if 2 > 1:
    print 21

34
'''),
    #############################################
    # with multi line strings
    ('''
def f(a, b):
    return a, b

for k in [1,2]:
    print k
abc = """This is a long...
long
   long text
"""
abc = """This is a long...
long
   long text"""
[1, 2]
''',  # -----------------------------------------
     '''
def f(a, b):
    return a, b

for k in [1,2]:
    print k

abc = """This is a long...
long
   long text
"""

abc = """This is a long...
long
   long text"""

[1, 2]
'''),
    #############################################
    # ignore sentences with syntax errors
    ('''
19
def (:
45
''',  # -----------------------------------------
     '''
19

45
'''),
    #############################################
]


@mark.parametrize("ipython_log_contents, sentences", contents_and_sentences)
def test_log_entries(ipython_log_contents, sentences):
    lines = StringIO.StringIO(ipython_log_contents).readlines()
    sentences = sentences.strip().split('\n\n')
    sentences.reverse()
    assert get_sentences(lines) == sentences
