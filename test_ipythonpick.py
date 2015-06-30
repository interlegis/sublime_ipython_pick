import sys
sys.modules['sublime'] = __import__('stub_sublime')
sys.modules['sublime_plugin'] = __import__('stub_sublime_plugin')
from ipythonpick import get_raw_log_entries  # noqa

# this was taken from an actual ipython_log.py file (with ipython==3.2.0)
ipython_log_contents = '''
# IPython log file


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
'''

raw_entries = '''
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
'''.strip().split('\n\n')
raw_entries.reverse()


def test_log_entries():

    assert get_raw_log_entries(ipython_log_contents) == raw_entries
