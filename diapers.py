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
  
def sim(state0,life=100,spy=False):
  t0 = 0
  for t in xrange(life):
    state1 = state0.copy()
    yield t - t0, t,state0,state1
    for key in state1.has().keys():
      if state1[key]  < 0:
        state1[key] = 0
    if spy:
      print(t,state0)
    state0 = state1
    t0 = t
  
def diapers():
  world = o(C=20, D=0,q=0, r=8, s=0)
  for dt,t,u,v in sim(world,life=60,spy=True):
    v.C +=  dt*(u.q - u.r)
    v.D +=  dt*(u.r - u.s)
    v.q  =  70 if t % 7 == 6 else 0 
    v.s  =  u.D if (t % 7 == 6) else 0
    if t == 27: # special case (the day i forget)
      v.s = 0

diapers()
