from __future__ import print_function
from __future__ import absolute_import, division
import pprint, traceback
"""

Simple container class (offers simple initialization).

"""
class o:
  def __init__(i,**d): i + d
  def __repr__(i)  : return str(has(i))
  def __add__(i,d) : i.__dict__.update(d); return i
  def __getitem__(i,k)   : return i.__dict__[k]
  def __setitem__(i,k,v) : i.__dict__[k] = v

def has(x):
  isa = isinstance
  if isa(x,list): return [has(v) for v in x]
  if isa(x,dict): return {k:has(v) for k,v
                          in x.items()
                          if k[0] != "_"}
  if isa(x,o): return {"o": has(x.__dict__)}
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
