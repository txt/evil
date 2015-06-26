from __future__ import division,print_function
from lib import *

@setting #########################################
def DSL(): return o(
  
) ################################################

def val(x): return x.val if isa(x,Thing) else x

class Thing(object):
  def __init__(i,txt="",init=0,lo=0,hi=1e32,prec=0,base=1):
    i.txt,i.val = txt,init
    i.lo, i.hi  = lo,hi
    i.prec,i.base= prec,base
  def restrain(i,x):
    if val(x) > i.hi : x = i.hi
    if val(x) < i.lo : x = i.lo
    return x
  def allows(i,j):
    return j.lo >= i.lo and j.hi <= i.hi
  def within(i,j):
    return i.lo <= j <= i.hi
  def any(i):
    x= i.lo + (i.hi - i.lo)*r()
    x= round(i.base*round(float(x)/i.base),i.prec)
    return int(x) if i.prec is 0 else x
  def norm(i,x):
    return (x - i.lo)/(i.hi - i.lo + i.tiny)
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
  def about(i): return o()
  def whatif(i): return o()
  def stop(i): False
  def start(i,n=1000,dt=1,report=50,verbose=True,inits={}):
    eden = i.maybes(i.about(),inits)
    keys,log  = i.header(eden)
    for t,v in i.run(eden,n,dt): 
      if not (t % report) and t > 0:
        log1 = [round(val(v[k]),1) for k in keys]
        log += [log1]
    if verbose: printm(log)
    return v
  def header(i,vars):
    keys = sorted(vars.keys())
    return  keys,[
             keys,
             [vars[k].__class__.__name__
                        for k in keys]]
  def maybe(i):
    return {k:v.any() for k,v in i.whatif().maybe.items()}
  def maybes(i,vars,inits):
    assert "_t" in vars.has() 
    for k,v in i.whatif().maybe.items(): 
      assert k in vars.has()
      assert vars[k].allows(v)
      tmp = v.any()
      if k in inits:
        if v.within(inits[k]):
          tmp = inits[k]
      vars[k].val = tmp
    return vars
  def goals(i):
    return i.whatif().goals.keys()
  def restrain(i,now,vars):
    for k,v in now.items():
      now[k] = vars[k].restrain(v)
  def run(i,about,n=100,dt=1):
    tnow = about
    t=0
    while t < n:
      tnext = tnow.copy()
      i.step(tnow,tnext,t,dt)
      tnext._t.val = t = t + dt
      i.restrain(tnext,about)
      yield t,tnext
      if i.stop(t,tnext):
        break
      tnow = tnext    
  
class BrooksLaw(Model):
  def stop(i,t,j):
    return val(j.r) <= 0 or t > 500 
  def whatif(i):
    return o(goals= o(_t  = lt,
                      ep  = lt,
                      r   = lt),
             maybe=o(ep   = Thing(lo=10,hi=50,base=5),
                     np   = Thing(lo=1,hi=10),
                     ts   = Thing(lo=3,hi=10),
                     r    = Thing(lo=100,hi=1000,base=50),
                     inc  = Thing(lo=1,hi=10),
                     early=Thing(lo=30,hi=90,base=7)))
  def about(i): return o(
    _t    = Aux("time"), 
    aR    = Flow(   "assimilationRate"),
    co    = Percent("communicationOverhead"),
    d     = Stock(  "developedSoftware",0),
    early = Aux(    "earlyInTheDevelopment",90),
    ep    = Stock(  "experiencedPeople",20),  
    ept   = Aux(    "experiencedPeopleNeeded2Train"),
    inc   = Aux(    "numberOfPeopleToAdd",2),    
    late  = Aux(    "defininitionLate",75),
    nprod = Aux(    "nominalProductity",0.1),
    np    = Stock(  "newPersonnel",0),
    paR   = Flow(   "personnelAllocationRate"),
    ps    = Aux(    "plannedSoftware"),
    sdR   = Flow(   "softwareDevelopmentRate"),
    ts    = Aux(    "teamSize",5),
    to    = Percent("trainingOverhead",25), # one-quarter of an experienced
                                          # person's time is needed to
                                          # train a new person until
                                          # he/she is fully assimilated.
    r     = Stock("requirements",500))
  
  def step(self,i,j,t,dt):
    def _co(x): 
      myTeam = 1*i.ts     # talk to everyone in my team
      others = x/i.ts   # talk to every other team
      return 0.06*(myTeam**2 + others**2) 
    j.aR  = i.np/20
    j.ps  = 2.5*t  
    j.co  = _co(i.ep + i.np)
    j.paR = i.inc if (i.ps - i.d) > i.late and t < i.early else 0
    j.sdR = i.nprod*(1-i.co/100)*(0.74*i.np+1.28*(i.ep - i.ept))
    j.ept = i.np*i.to /100
    j.ep += i.aR*dt
    j.np += (i.paR - i.aR)*dt
    j.d  += i.sdR*dt
    j.r  +=  - i.sdR*dt
