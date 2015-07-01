from __future__ import print_function,division
from run import *

class Diapers(Simulation):
  def things(i): return  Things(
    T= Time(hi=100),
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

class BrooksLaw(Simulation):
  def earlyStop(i,state): 
    return state.r <= 1 #or state.T > 1000 
  def things(i):
    return Things( 
    T     = T(hi=1000,step=1), 
    aR    = F("assimilationRate"),
    co    = A("communicationOverhead",
              lo=0,hi=100),    
    d     = S("developedSoftware",
              init=0),
    early = A("earlyInTheDevelopment",
              init=100,touch=True,lo=30,hi=300,step=1),
    ep    = S("experiencedPeople",
              init=30,lo=10,hi=100,goal=lt,touch=True),  
    ept   = A("experiencedPeopleNeeded2Train"),
    inc   = A("numberOfPeopleToAdd",  
              init=10,touch=True,lo=0,hi=20),    
    late  = A("defininitionLate",
              init=50,touch=True,lo=5,hi=100),
    nprod = A("nominalProductity",
              init=0.1), 
    np    = S("newPersonnel",
              init=0,lo=0,hi=10),
    paR   = F("personnelAllocationRate"),
    ps    = A("plannedSoftware"),
    sdR   = F("softwareDevelopmentRate"),
    ts    = A("teamSize",
              init=5,touch=True,lo=1,hi=10),
    to    = A("trainingOverhead",
              init=25,lo=0,hi=100), 
    r     = S("requirements",
              init=500,goal=gt,lo=0,touch=False,hi=1000))
  
  def step(self,dt,t,u,v): 
    def _co(x): 
      myTeam = u.ts     # talk to everyone in my team
      others = x/u.ts   # talk to every other team
      return 0.06*(myTeam + others-2)**2 #myTeam**2 + others**2)
      #return 0.06*(x**2) #myTeam**2 + others**2) 
    u.inc = 0 if t < 21 else u.inc # dont cry late for at least 3 weeks
    v.aR  = u.np/10 
    v.ps  = 5*t #5
    v.co  = _co(u.ep + u.np)
    v.paR = u.inc if u.co < 50 and (u.ps - u.d) > u.late and t < u.early else 0
    v.sdR = u.nprod*(1-u.co/100)*(0.8*u.np + 1.2*(u.ep - u.ept))
    v.ept = u.np*u.to /100
    v.ep += u.aR*dt
    v.np += (u.paR - u.aR)*dt
    v.d  += u.sdR*dt
    v.r  +=  - u.sdR*dt
  
