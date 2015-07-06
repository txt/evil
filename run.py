from __future__ import print_function,division
from lib import *
from cols import *


class Has(object):
  def __init__(i,name='',lo=0,hi=1e32,init=0,
               obj=lambda it: i.ok(it),
               goal=None,step=1,prec=2,touch=False):
    i.name,i.lo,i.hi      = name,lo,hi
    i.init,i.goal,i.touch = init,goal,touch
    i.step,i.prec         = step,prec
    i.obj                 = obj
  def show(i,x):
    return round(x,i.prec) if i.prec > 0 else int(x)
  def restrain(i,x):
    if   x < i.lo: return i.lo
    elif x > i.hi: return i.hi
    else:
      return x
  def any(i):
    return within(i.lo,i.hi)
  def ok(i,x):
    return i.lo <= x <= i.hi
  def __repr__(i):
    return '%s=%s' % (i.name, o(name=i.name,obj=i.obj.__name__,lo=i.lo,hi=i.hi,init=i.init,goal=i.goal,step=i.step,prec=i.prec,touch=i.touch))

class Flow(Has): pass
class Stock(Has): pass
class Aux(Has): pass
class Time(Has):
  def __init__(i,lo=0,hi=1e32,step=1,prec=0,goal=None,touch=False):
    super(Time,i).__init__(name='time',lo=lo,
                           hi=hi,step=step,prec=prec,goal=goal,touch=touch)

F,A,S,T=Flow,Aux,Stock,Time

class Have:
  def __init__(i,ok=lambda z: True, **cells):
    i.keys = i.order(cells.keys(),'T')
    i.objs = {k:v for k,v in cells.items() if v.goal}
    i.decs = {k:v for k,v in cells.items() if not v.goal}
    i.ok   = ok
    i.cells = cells
  def __iadd__(i,has):
    i.cells[has.name] = has
    return Have(**i.cells)
  def ok(i,it):
    for k,v in i.decs:
      if not v.ok(it[k]):
        return False
    return True
  def objectives(i,it):
    for k,v in i.objs.items():
      it[k] = v.obj(it)
    return it
  def order(i,keys,first):
    pre = [first] if first in keys else []
    return pre + sorted(k for k in keys if k != first)
  def show(i, it):
    return [i.cells[k].show(it[k])
            for k in i.keys]
  def init(i,d={}):
    tmp= o(**{k:v.init
                for k,v in i.cells.items()})
    for k,v in d.items():
      tmp[k] = v
    return tmp
  def restrain(i,it):
    for k,v in it.items():
      has = i.cells[k]
      if   v < has.lo: it[k] = has.lo
      elif v > has.hi: it[k] = has.hi
    return it
  def duration(i):
    assert 'T' in i.cells
    t0 = t = i.cells['T'].lo
    while t < i.cells['T'].hi:
      t += i.cells['T'].step
      yield t - t0, t
      t0 = t

def crossover(cells,a,b,c,f=0.5,cr=0.5,cxt={},go=1):
  assert go < 16,('%s too goes' % go)
  it=a.copy()
  messable=[]
  for k,v in cells.decs.items():
    if v.touch:
      if k in cxt:
         it[k] = cxt[k].any()
      else:
         messable += k
         if r() < cr:
           one = a[k] + f*(b[k] - c[k])
           two = wrap(one,v.lo,v.hi)
           it[k] = two
  if messable:
     it[k] = a[any(messable)]
  return it if cells.ok(it) else crossover(cells,
                                         a,b,c,f,cr,
                                         cxt,go+1)

def mutate(cells,it0,cxt={},p= 0.3,go=1):
  assert go < 16,('%s too many goes' % go)
  it1 = it0.copy()
  for k,v in cells.decs.items():
    if v.touch:
      if k in cxt:
        it1[k] = cxt[k].any()
      elif r() < p:
        it1[k] =  v.any()
  return it1 if cells.ok(it1) else mutate(cells,it0,p,go+1)

def decisions(cells,cxt={},go=1):
  assert go < 16,('%s too many goes' % go)
  it=o()
  for k,v in cells.decs.items():
    if v.touch:
      if k in cxt:
        it[k] = cxt[k].any()
      else: 
        it[k] = v.any() 
    else:
      it[k] = v.init
  return it if cells.ok(it) else decisions(cells,d,go+1)

class Haves:
  def __init__(i,cells,steps=20):
    i.log,i.cells,i.steps = [],cells,steps
    i.nums = {k:Nums() for k in i.cells.keys}
    i.scores = Nums()
  def normalize(i,it):
    def norm(x,v):
      return (x - v.lo)/(v.hi - v.lo + -1e32)
    norms = {k:norm(it[k],v)
             for k,v in i.nums.items()}
  def evaluateLogScore(i,it):
     x = i.cells.objectives(it)
     i.add(x)
     return x,i.aggregate(x)
  def another(i):
    return i.evaluateLogScore(i.cells.decisions())
  def amutant(i,it,p=0.25):
    return i.evaluateLogScore(i.cells.mutate(it,p))
  def aggregate(i,it):
    sum = all = 0
    for k,v in i.cells.objs.items():
      it1 = it[k]
      num    = i.nums[k]
      has1 = i.cells.cells[k]
      all   += 1
      norm = (it1 - num.lo)/(num.hi - num.lo + 0.0001)
      if has1.goal == lt:
         norm = 1 - norm
      sum += norm**2
    s=  1 - sqrt(sum)/sqrt(all) # by convention, lower aggregate scores are better
    return s
  def add(i,it):
    for k,v in i.nums.items():
      v += it[k]
    if i.steps:
      i.log += [i.cells.show(it)]
    return i
  def dump(i):
    if i.log:
      m = [i.cells.keys] + i.log[0::i.steps]+[i.log[-1]]
      printm(ditto(m," "))
      i.log = []

def printm(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = ' | '.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)



class Simulation:
  def cells(i):
    return Have(T= A('time',init=0,lo=0,hi=100))
  def step(i,dt,t,u,v): pass
  def earlyStop(i,it): return False
  def run(i,spy=20,verbose=True,whatif={}):
    cells = i.cells()
    log    = Haves(cells,spy)
    it1 = it0 = cells.init(whatif)
    for dt,t in cells.duration():
      it0.T = t
      it1 = it0.copy()
      i.step(dt,t,it0,it1)
      it1 = cells.restrain(it1)
      it0 = it1
      log   += it1
      if i.earlyStop(it1):
        break
    if verbose:
      log.dump()
    return it1

class Function:
  def cells(i): return Have()
  def step(i,it): pass
  def earlyStop(i,it): pass
