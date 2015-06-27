from __future__ import print_function,division

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
  def __init__(i,**d) : i.has().update(d)
  def copy(i)         : return o(**i.has().copy())
  def __getitem__(i,k): return i.has()[k]
  def __setitem__(i,k,v):      i.has()[k] = v
  def __repr__(i)     : return 'o'+str(i.has())
  
def sim(state0,life=100,spy=False,dt=1):
  t= 0
  while t < life:
    t += dt
    state1 = state0.copy()
    yield dt, t,state0,state1
    state0 = state1
    for key in state1.has().keys():
      if state1[key]  < 0:
        state1[key] = 0
    if spy:
      print(t,state1)
  
def diapers():
  def saturday(x): return int(x) % 7 == 6
  world = o(C=20, D=0,q=0, r=8, s=0)
  for dt,t,u,v in sim(world,life=60,spy=True,dt=0.5):
    v.C +=  dt*(u.q - u.r)
    v.D +=  dt*(u.r - u.s)
    v.q  =  70 if saturday(t) else 0 
    v.s  =  u.D if saturday(t) else 0
    if t == 27: # special case (the day i forget)
      v.s = 0

diapers()
