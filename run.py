from __future__ import print_function,division
from lib import *

class Thing(object):
  def __init__(i,name='',lo=0,hi=1e32,init=0,
               goal=None,step=1,prec=2,touch=False):
    i.name,i.lo,i.hi      = name,lo,hi
    i.init,i.goal,i.touch = init,goal,touch
    i.step,i.prec         = step,prec
  def show(i,x):
    x = round(x,i.prec)
    if i.prec == 0:
      x = int(x)
    return x
  def restrain(i,x):
    if   x < i.lo: return i.lo
    elif x > i.hi: return i.hi
    else:
      return x
  def __repr__(i): return '%s=%s' % (i.name, o(name=i.name,lo=i.lo,hi=i.hi,init=i.init,goal=i.goal,step=i.step,prec=i.prec,touch=i.touch))

class Flow(Thing): pass
class Stock(Thing): pass
class Aux(Thing): pass
class Time(Thing):
  def __init__(i,lo=0,hi=1e32,step=1,prec=0,goal=None,touch=False):
    super(Time,i).__init__(name='time',lo=lo,
                           hi=hi,step=step,prec=prec,goal=goal,touch=touch)

F,A,S,T=Flow,Aux,Stock,Time

class Things:
  def __init__(i,**things):
    i.keys = i.order(things.keys(),'T')
    i.things = things
  def order(i,keys,first):
    assert first in keys, "state needs time 'T'"
    return [first] + sorted(k for k in keys if k != first)
  def show(i, state):
    return [i.things[k].show(state[k])
            for k in i.keys]
  def any(i):
    def any1(v):
      return round(within(v.lo,v.hi)) if  v.touch else v.init
    return o(**{k:any1(v)
                for k,v in i.things.items()})
  def init(i,d={}):
    tmp= o(**{k:v.init
                for k,v in i.things.items()})
    for k,v in d.items():
      tmp[k] = v
    return tmp
  def restrain(i,state):
    for k,v in state.items():
      thing = i.things[k]
      if   v < thing.lo: state[k] = thing.lo
      elif v > thing.hi: state[k] = thing.hi
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
    return i
  def dump(i):
    if i.log:
      printm([i.things.keys] + i.log[0::i.steps]+[i.log[-1]])
      i.log = []

def printm(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = ' | '.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)
    

class Simulation:
  def things(i):
    return Things(T= A('time',init=0,lo=0,hi=100))
  def step(i,dt,t,u,v): pass
  def earlyStop(i,state): return False
  def run(i,spy=20,verbose=True,whatif={}):
    things = i.things()
    log    = Log(things,spy)
    state1 = state0 = things.init(whatif)
    for dt,t in things.duration():
      state0.T = t
      state1 = state0.copy()
      i.step(dt,t,state0,state1)
      state1 = things.restrain(state1)
      state0 = state1
      log += state1
      if i.earlyStop(state1):
        break
    if verbose:
      log.dump()
    return state1
