# -*- coding: utf-8 -*-
import StringIO
import sys

from pytest import mark


try:
    from ipythonpick import get_sentences, get_summarized_sentences
except ImportError, e:
    # mock module dependencies not relevant to the tests
    # (only if we're really out of sublime environment)
    if e.message in ['No module named %s' % name
                     for name in ['sublime', 'sublime_plugin']]:
        import stubmodule_sublime
        import stubmodule_sublime_plugin
        sys.modules['sublime'] = stubmodule_sublime
        sys.modules['sublime_plugin'] = stubmodule_sublime_plugin
    from ipythonpick import get_sentences, get_summarized_sentences


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
''',  # -----------------------------------------
     '''
def f(a, b):
    return a, b

for k in [1,2]:
    print k

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
a = 2
a = 3
''',  # -----------------------------------------
     '''
19

45

a = 2

a = 3
''',  # -----------------------------------------
     '''
19

45

a = 3
'''),
    #############################################
]


@mark.parametrize("ipython_log_contents, sentences, summarized", contents_and_sentences)
def test_log_entries(ipython_log_contents, sentences, summarized):

    def split_expected(sentences):
        sentences = sentences.strip().split('\n\n')
        sentences.reverse()
        return sentences

    lines = StringIO.StringIO(ipython_log_contents).readlines()
    sentences, summarized = map(split_expected, (sentences, summarized))

    assert get_sentences(lines) == sentences
    assert get_summarized_sentences(lines) == summarized
