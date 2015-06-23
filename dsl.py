from __future__ import division,print_function
from lib import *

@setting #########################################
def DSL(): return o(
  
) ################################################



def val(x): return x.val if isa(x,Thing) else x

class Thing(object):
  def __init__(i,txt,init=0,lo=0,hi=1e32):
    i.txt,i.val = txt,init
    i.lo, i.hi  = lo,hi
  def restrain(i,x):
    if val(x) > i.hi : x = i.hi
    if val(x) < i.lo : x = i.lo
    return x
  def __trunc__(i)      : return int(i.val)
  def __add__(i,j)      : return i.val + val(j)
  def __sub__(i,j)      : return i.val - val(j)
  def __mul__(i,j)      : return i.val * val(j)
  def __div__(i,j)      : return i.val / val(j)
  def __truediv__(i,j)  : return i.val / val(j)
  def __pos__(i)        : return i.val
  def __neg__(i)        : return - i.val 
  def __radd__(j,i)     : return val(i) + j.val
  def __rsub__(j,i)     : return val(i) - j.val
  def __rmul__(j,i)     : return val(i) * j.val
  def __rdiv__(j,i)     : return val(i) / j.val
  def __rtruediv__(j,i) : return val(i) / j.val
  def __repr__(i): return '<%s=%g>' % (i.txt,i.val)

class Aux(Thing):   pass
class Flow(Thing):  pass
class Stock(Thing): pass
class Percent(Aux):
  def __init__(i,txt,init=0):
    super(Percent, i).__init__(txt,init,0,100)
      
class Model(object):
  def run(i,n=1000,dt=1,report=50):
    eden = i.reset()
    keys = sorted(eden.has().keys())
    head = ['tick'] + keys
    log  = [head]
    for t,v in i.steps(n,dt,eden):
      if not (t % report) and t > 0:
        log1 = [t] + [round(val(v[k]),1) for k in keys]
        log += [log1]
    printm(log)
  def reset(i):
    return o()
  def restrain(i,now,vars):
    for k,v in now.has().items():
      now[k] = vars[k].restrain(v)
  def steps(i,n=100,dt=1,tfirst=None):
    if tfirst is None: tfirst = i.reset()
    tnow = tfirst
    for t in xrange(n):
      tnext = tnow.copy()
      i.step(tnow,tnext,t,dt)
      i.restrain(tnext,tfirst)
      yield t,tnext
      if val(tnext.r) <= 0:
        print("done",t)
        break
      tnow = tnext

class BrooksLaw(Model):
  def reset(i): return o(
    aR    = Flow( "assimilationRate"),
    co    = Percent(  "communicationOverhead"),
    d     = Stock("developedSoftware",0),
    ep    = Stock("experiencedPeople",20),  
    ept   = Aux(  "experiencedPeopleNeeded2Train"),  
    nprod = Aux(  "nominalProductity",0.1),
    np    = Stock("newPersonnel",0),
    paR   = Flow( "personnelAllocationRate"),
    ps    = Aux(  "plannedSoftware"),
    sdR   = Flow( "softwareDevelopmentRate"),
    ts    = Aux("teamSize",5),
    to    = Percent( "trainingOverhead",25), # one-quarter of an experienced
                                          # person's time is needed to
                                          # train a new person until
                                          # he/she is fully assimilated.
    r     = Stock("requirements",500))
  
  def step(self,i,j,t,dt):
    def _co(x): 
      myTeam = i.ts - 1   # talk to everyone in my team
      others = x/i.ts - 1 # talk to every other team
      return 0.06*(myTeam**2 + others**2) 
    j.aR  = i.np/20
    j.ps  = 2.5*t  
    j.co  = _co(i.ep + i.np)
    j.paR = 4 if (i.d - i.ps) < 75 and t < 60 else 0
    j.sdR = i.nprod*(1-i.co/100)*(0.74*i.np+1.28*(i.ep - i.ept))
    j.ept = i.np*i.to /100
    j.ep += i.aR*dt
    j.np += (i.paR - i.aR)*dt
    j.d  += i.sdR*dt
    j.r  +=  - i.sdR*dt
