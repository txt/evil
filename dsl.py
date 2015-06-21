from __future__ import division
from lib import *

@setting #########################################
def DSL(): return o(
  
) ################################################

def val(x): return x.val() if isa(x,Thing) else  x


def add(x,y): return x+y
def sub(x,y): return x-y
def mul(x,y): return x*y
def div(x,y): return x/y
def mod(x,y): return x // y
def pow(x,y): return x**y

  
# amke this the roor of all
class Thing:
  def __init__(i,txt,init=100,model=None):
    i.model = model or Model.latest()
    i.txt =txt
    i.model.add(i)
    i.equation= init
  def __repr__(i):
    return "%s=%s" % (i.txt, i.equation)
  def __iadd__(i,eq):
    i.equation = eq
  def __add__( i,j): return Eq(i,j,add)
  def __sub__( i,j): return Eq(i,j,sub)
  def __mul__( i,j): return Eq(i,j,mul)
  def __div__( i,j): return Eq(i,j,div)
  def __mod__( i,j): return Eq(i,j,mod)
  def __pow__( i,j): return Eq(i,j,pow)
  def __radd__(i,j): return Eq(j,i,add)
  def __rsub__(i,j): return Eq(j,i,sub)
  def __rmul__(i,j): return Eq(j,i,mul)
  def __rdiv__(i,j): return Eq(j,i,div)
  def __rmod__(i,j): return Eq(j,i,mod)
  def __rpow__(i,j): return Eq(j,i,pow)
  
"""
In my personal opinion this would not be a great
idea in production code: the biggest problem with it
is that it totally non-standard and will probably
leave non-familiar readers wondering where this
novel syntax has suddenly sprung from.
"""
class Model:
  all = []
  @staticmethod
  def latest(): return Model.all[-1]
  def __init__(i,txt,tick=1):
    i.txt,i.tick = txt,tick
    i.t,i.parts,i.all=0,{},{}
  def add(i,p):
    klass          = p.__class__.__name__
    instances      = i.parts.get(klass,{})
    i.all[p.txt]   = instances[p.txt] = p
    i.parts[klass] = instances

@contextmanager
def model(name,w=None):
  w = w or o()
  m = Model(name)
  Model.all += [m]
  yield m,Stock,Flow,Auxillary
  Model.all.pop()


class Eq:
  def __init__(i,l,r,op) :
    i.tree = [op,l,r]
  def __repr__(i):
    op,l,r = i.tree
    return '%s(%s, %s)' % (op.__name__, l, r)
  def val(i) : return i.val1(i.tree,{})
  def val1(i,x,path) :
    assert not id(i) in path, "loop detected"
    path[id(i)] = i
    if isinstance(x,lst):
      op,left,right = lst
      return op(i.val1(left), i.val1(right))
    elif isintance(x,Thing):
      return x.val
    else:
      return x

class Stock(Thing): pass
class Flow(Thing): pass
class Auxillary(Thing): pass

def brooksLaw(w=None):
  with model("Brooks' Law",w) as (m,S,F,A):
    a     = F("assimilationRate")
    c     = A("communicationOverhead")
    d     = S("developedSoftware")
    ep    = S("experiencedPersonnel")
    ept   = A("experiencedPersonnelNeeded4Training")
    nprod = A("nominalProductity")
    np    = S("newPersonnel")
    por   = F("personnelAllocationRate")
    ps    = A("plannedSoftware")
    sd    = F("softwareDevelopmentRate")
    sr    = S("source",1e32)
    t     = A("trainingOverhead")
    r     = S("requirements")
    d    += r * sd
    sd   += np * np * ep * c
  return m    

