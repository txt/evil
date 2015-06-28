from __future__ import print_function,division
from contextlib import contextmanager

# duner. using numbers and sample.

"""

 q   +-----+  r  +-----+
---->|  C  |---->|  D  |--> s
 ^   +-----+     +-+---+
 |                 |
 +-----------------+ 

C = stock of clean diapers
D = stock of dirty diapers
q = inflow of clean diapers
r = flow of clean diapers to dirty diapers
s = out-flow of dirty diapers

"""
class o:
  def has(i)          : return i.__dict__
  def keys(i)         : return i.has().keys()
  def items(i)        : return i.has().items()
  def __init__(i,**d) : i.has().update(d)
  def copy(i)         : return o(**i.has().copy())
  def __getitem__(i,k): return i.has()[k]
  def __setitem__(i,k,v): i.has()[k] = v
  def __repr__(i)     : return 'o'+str(i.has())

class Thing(object):
  def __init__(i,name='',lo=0,hi=1e32,init=0,
               goal=None,step=1,prec=0):
    i.name,i.lo,i.hi= name,lo,hi
    i.init,i.goal   = init,goal
    i.step,i.prec   = step,prec
  def show(i,x):
    x= round(i.step*round(x/i.step),i.prec)
    if i.prec == 0:
      x = int(x)
    return x
  def restrain(i,x):
    if   x < i.lo: return i.lo
    elif x > i.hi: return i.hi
    else:
      return x

class Flow(Thing): pass
class Stock(Thing): pass
class Aux(Thing): pass
class Time(Thing):
  def __init__(i,lo=0,hi=1e32,step=1,prec=0):
    Thing.__init__(name='time',lo=lo,
                   hi=hi,step=step,prec=prec)

F,A,S,T=Flow,Aux,Stock,Time

class Things:
  def __init__(i,**things):
    i.keys = ['T'] + i.order(things.keys(),'T')
    i.things = things
  def order(i,keys,first):
    assert first in keys
    return [first] + sorted(k for k in keys if k != first)
  def show(i, state):
    return [i.things[k].show(state[k])
            for k in i.keys]
  def init(i):
    return o(**{k:v.init
                for k,v in i.things.items()})
  def restrain(i,state):
    for k,v in state.items():
      thing = i.things[k]
      if   v < thing.lo: state[k] = thing.lo
      elif v > thing.hi: state[k] = think.hi
    return state
  def duration(i):
    assert 'T' in i.things
    t0 = t = i.things['T'].lo
    while t < i.things['T'].hi:
      t += i.things['T'].step
      yield t - t0, t
      t0 = t
      
class Log:
  def __init__(i,things,steps=20):
    i.log,i.things,i.steps = [],things,steps
  def __iadd__(i,state):
    if i.steps:
      i.log += [i.things.show(state)]
      if len(i.log) % i.steps == 0:
        i.dump()
    return i
  def dump(i):
    if i.log:
      print("")
      printm(i.things.keys() + i.log)
      i.log = []

def printm(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = ' | '.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)
    
def sim(things,spy=0):
  state0 = things.init()
  log    = Log(things,spy)
  for dt,t in things.duration():
    state0.T = t
    log   += state0
    state1 = state0.copy()
    yield dt,t,state0,state1
    state1 = things.restrain(state1)
    state0 = state1
  log.dump()

class Simulation:
  def things(i):
    return Things(T= A('time',init=0,lo=0,hi=100))
  def step(i,dt,t,u,v): pass
  def earlyStop(i,state): return False
  def run(i):
    for dt,t,u,v in sim(i.things(),spy=20):
      i.step(dt,t,u,v)
      if i.earlyStop(v):
        break
      
class Diapers(Simulation):
  def things(i): return  Things(
    T= A('time',           init=0, lo=0, hi=100),
    C= S('clean',          init=20,lo=0, hi=1000),
    D= S('dirty',          init=0, lo=0, hi=1000),
    q= F('new clean',      init=0, lo=0, hi=200),
    r= F('clean2dirty',    init=8, lo=0, hi=100),
    s= F('departing dirty',init=0, lo=0, hi=100)
    )
  def step(i,dt,t,u,v):
    def saturday(t):
      return t % 7 == 6
    v.C +=  dt*(u.q - u.r)
    v.D +=  dt*(u.r - u.s)
    v.q  =  70  if saturday(t) else 0 
    v.s  =  u.D if saturday(t) else 0
    if int(t) == 27: # special case (the day i forget)
      v.s = 0

Diapers().run()
