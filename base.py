from __future__ import print_function
from __future__ import absolute_import, division
import pprint, traceback
"""

Simple container class (offers simple initialization).

"""
class o:
  def __init__(i,**d): i.has().update(d)
  def __repr__(i)  : return 'o'+str(has(i))
  def __add__(i,d) : i.__dict__.update(d); return i
  def __getitem__(i,k)   : return i.has()[k]
  def __setitem__(i,k,v) : i.has()[k] = v
  def copy(i): return o(**i.has().copy())
  def has(i) : return i.__dict__
  def keys(i): return i.__dict__.keys()
  def items(i): return i.__dict__.items( )
  
def has(x):
  isa = isinstance
  if isa(x,list): return [has(v) for v in x]
  if isa(x,dict): return {k:has(v) for k,v
                          in x.items()
                          if k[0] != "_"}
  if isa(x,o): return {"o": has(x.__dict__)}
  if isa(x,float): return '%g' % x
  return x

def pretty(x): print(pprint.pformat(x))

def show(x, indent=None, width=None):  
  print(pprint.pformat(has(x),
            indent= indent or the.LIB.show.indent,
            width = width  or the.LIB.show.width))
"""

The settings system.

"""
the = o()

def setting(f):
  name = f.__name__
  def wrapper(**d):
    tmp = f()
    tmp + d
    the[name] = tmp
    return tmp
  wrapper()
  return wrapper

def default(v1,v2):
  return v2 if v1 is None else v1
