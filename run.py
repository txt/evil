from __future__ import print_function,division
from lib import *
from cols import *

def noop(x): return x

class Thing(object):
  def __init__(i,name='',lo=0,hi=1e32,init=0,
               obj=noop,
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
  def mutate(i):
    return within(i.lo,i.hi)
  def __repr__(i):
    return '%s=%s' % (i.name, o(name=i.name,obj=i.obj.__name__,lo=i.lo,hi=i.hi,init=i.init,goal=i.goal,step=i.step,prec=i.prec,touch=i.touch))

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
    i.objs = {k:v for k,v in things.items() if v.goal}
    i.decs = {k:v for k,v in things.items() if not v.goal}
    i.things = things
  def __iadd__(i,thing):
    i.things[thing.name] = thing
    return Things(**i.things)
  def objectives(i,state):
    for k,v in i.objs.items():
      state[k] = v.obj(state)
    return state
  def order(i,keys,first):
    pre = [first] if first in keys else []
    return pre + sorted(k for k in keys if k != first)
  def show(i, state):
    return [i.things[k].show(state[k])
            for k in i.keys]
  def mutate(i,state,p= 0.3):
    out = state.copy()
    for k,v in i.decs.items():
      if r() < p:
        out[k] =  v.mutate()
    assert out.has().values() != state.has().values()
    return out
  def decisions(i,d={}):
    def decision(k,v):
      if v.touch:
        v = d[k].any1() if v in d else within(v.lo,v.hi)
      elif not v.goal:
        v = v.init
      return v
    return o(**{k:decision(k,v)
                for k,v in i.decs.items()})
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
    i.nums = {k:Nums() for k in i.things.keys}
    i.scores = Nums()
  def normalize(i,state):
    def norm(x,v):
      return (x - v.lo)/(v.hi - v.lo + -1e32)
    norms = {k:norm(state[k],v)
             for k,v in i.nums.items()}
  def evaluateLogScore(i,state):
     x = i.things.objectives(state)
     i += x
     return x,i.score(x)
  def another(i):
    return i.evaluateLogScore(i.things.decisions())
  def amutant(i,state,p=0.25):
    return i.evaluateLogScore(i.things.mutate(state,p))
  def score(i,state):
    sum = all = 0
    for k,v in i.things.objs.items():
      state1 = state[k]
      num    = i.nums[k]
      thing1 = i.things.things[k]
      all   += 1
      norm = (state1 - num.lo)/(num.hi - num.lo + 0.0001)
      if thing1.goal == lt:
         norm = 1 - norm
      sum += norm**2
    s=  1 - sqrt(sum)/sqrt(all) # by convention, lower scores are better
    return s
  def __iadd__(i,state):
    for k,v in i.nums.items():
      v += state[k]
    if i.steps:
      i.log += [i.things.show(state)]
    return i
  def dump(i):
    if i.log:
      m = [i.things.keys] + i.log[0::i.steps]+[i.log[-1]]
      printm(ditto(m," "))
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
      log   += state1
      if i.earlyStop(state1):
        break
    if verbose:
      log.dump()
    return state1

class Function:
  def things(i): return Things
  def step(i,state): pass
  def earlyStop(i,state): pass
