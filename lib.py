from __future__ import print_function
from __future__ import absolute_import, division
import random, re, datetime, time,pprint,sys
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
r    = random.random
any  = random.choice
seed = random.seed
isa  = isinstance
fun  = lambda x: x.__class__.__name__ == 'function'

def lt(x,y): return x < y
def gt(x,y): return x > y
def first(lst): return lst[0]
def last(lst): return lst[-1]
                          
def shuffle(lst):
  random.shuffle(lst)
  return lst

def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9],
                norm=False, f=3):
  if norm:
    lo,hi = lst[0], lst[-1]
    lst= g([(x - lo)/(hi-lo+0.0001) for x in lst],f)
  at = lambda x: lst[ int(len(lst)*x) ]
  lst = [ at(tile) for tile in tiles ]
  
  return lst

def say(*lst):
  sys.stdout.write(', '.join(map(str,lst)))
  sys.stdout.flush()

def g(lst,f=3):
  return map(lambda x: round(x,f),lst)
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
  seed(the.LIB.seed)            
  show(the)                   
  with duration():
    yield
  for (using,_) in usings:
    using()               
