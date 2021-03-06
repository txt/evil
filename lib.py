from __future__ import print_function
from __future__ import absolute_import, division
import random, re, datetime, time,pprint,sys,math
from contextlib import contextmanager
from base import *

@setting #########################################
def LIB(): return o(
  seed = 1,
  has  = o(decs = 3,
           skip="_",
           wicked=True),
  show = o(indent=2,
           width=50)
) ################################################
"""

Unit test engine, inspired by Kent Beck.

"""
def ok(*lst):
  for one in lst: unittest(one)
  return one

class unittest:
  tries = fails = 0  #  tracks the record so far
  @staticmethod
  def score():
    t = unittest.tries
    f = unittest.fails
    return "# TRIES= %s FAIL= %s %%PASS = %s%%"  % (
      t,f,int(round(t*100/(t+f+0.001))))
  def __init__(i,test):
    unittest.tries += 1
    try:
      test()
    except Exception,e:
      unittest.fails += 1
      i.report(e,test)
  def report(i,e,test):
    print(traceback.format_exc())
    print(unittest.score(),':',test.__name__, e)

#-------------------------------------------------

now  = datetime.datetime.now
r    = random.random
any  = random.choice

isa  = isinstance
sqrt = math.sqrt
log  = math.log
e    = math.e
pi= math.pi
sin  = math.sin
fun  = lambda x: x.__class__.__name__ == 'function'
milli_time = lambda: int(round(time.time() * 1000))

def rseed(seed):
  if seed is not None: random.seed(seed)
def lt(x,y): return x < y
def gt(x,y): return x > y
def first(lst): return lst[0]
def last(lst): return lst[-1]
def mean(lst): return sum(lst)/len(lst)

def within(lo,hi): return lo + (hi - lo)*r()
def wrap(x,lo,hi):
  return x if x==hi else lo + (x - lo) % (hi - lo)

def shuffle(lst):
  random.shuffle(lst)
  return lst

def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9],
                norm=False, f=3,ordered=True):
  def pos(x):
    return len(lst) - 1 if x == 1 else int(len(lst)*x)
  assert len(lst) > len(tiles),"list too small"
  if not ordered:
    lst = sorted(lst)
  if norm:
    lo,hi = lst[0], lst[-1]
    lst= [(x - lo)/(hi-lo+0.0001) for x in lst]
  at = lambda x: lst[ pos(x) ]
  return g([ at(tile) for tile in tiles ],f)

def say(*lst):
  sys.stdout.write(', '.join(map(str,lst)))
  sys.stdout.flush()

def g(lst,f=3):
  return map(lambda x: round(x,f),lst)

def items(x): 
  if isinstance(x,(list,tuple)):
    for y in x:
      for z in items(y):
        yield z
  else:
     yield x

def printm(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = ' | '.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)

def ditto(m,mark="."):
  def worker(lst):
    out = []
    for i,now in enumerate(lst):
      before = old.get(i,None) # get old it if exists
      out += [mark if before == now else now]
      old[i] = now # next time, 'now' is the 'old' value
    return out # the lst with ditto marks inserted
  old = {}
  return [worker(row) for row in m]
  
#-------------------------------------------------

def cache(f):
  name = f.__name__
  def wrapper(i):
    i._cache = i._cache or {}
    key = (name, i.id)
    if key in i._cache:
      x = i._cache[key]
    else:
      x = f(i) # sigh, gonna have to call it
    i._cache[key] =  x # ensure ache holds 'c'
    return x
  return wrapper

@contextmanager
def duration():
  t1 = time.time()
  yield
  t2 = time.time()
  print("\n" + "-" * 72)
  print("# Runtime: %.3f secs" % (t2-t1))

def use(x,**y): return (x,y)

@contextmanager
def settings(*usings):
  for (using, override) in usings:
    using(**override)
  yield
  for (using,_) in usings:
    using()
    
@contextmanager
def study(what,*usings):
  print("\n#" + "-" * 50,
        "\n#", what, "\n#",
        datetime.datetime.now().strftime(
          "%Y-%m-%d %H:%M:%S"))    
  for (using, override) in usings:
    using(**override)              
  rseed(the.LIB.seed)
  show(the)                   
  with duration():
    yield
  for (using,_) in usings:
    using()               
