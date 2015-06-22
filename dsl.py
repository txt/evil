from __future__ import division
from lib import *

@setting #########################################
def DSL(): return o(
  
) ################################################


class Thing:
  def __init__(i,txt,init=0):
    i.txt,i,val = txt,init
    
class Aux(Thing):   pass
class Flow(Thing):  pass
class Stock(Thing): pass

class Model:
  def run(i,steps=100):
    next = lambda d: o(d.__dict__.copy())
    i.data = i.vars()
    tnow = next(i.data.__dict__)
    yield 0,tnow
    for t in xrange(steps):
      tnext = next(tnow)
      i.step(tnow,tnext,1)
      yield t,tnext
      tnow = tnext

class BrooksLaw(Model):
  def vars(i): return o(
    time  = Aux(  "time",0),
    aR    = Flow( "assimilationRate"),
    c     = Aux(  "communicationOverhead"),
    d     = Stock("developedSoftware",0)
    ep    = Stock("experiencedPeople",20),
    ept   = Aux(  "experiencedPeopleNeeded2Train"),
    nprod = Aux(  "nominalProductity"),
    np    = Stock("newPersonnel"),
    poR   = Flow( "personnelAllocationRate"),
    ps    = Aux(  "plannedSoftware"),
    sdR   = Flow( "softwareDevelopmentRate"),
    sr    = Stock("source",1e32),
    t     = Aux(  "trainingOverhead"),
    r     = Stock("requirements"))
  def step(self,i,j,dt):
    j.d  += i.srd*dt
    j.ep += i.aR*dt
    j.np += (i.pOR - i.aR)*dt
    j.paR = 10 if ((i.d - i.ps) < 75) and i.time < 112 else 0
    j.aR  = i.np/20
    j.r  +=  - i.sdR*dt
    j.sdR = nProd
    
