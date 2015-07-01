from  __future__ import print_function, division
from lib import *
from run import *

class Kursawe(Function):
  def f1(i,state):
    return state['0']
  def f2(i,state):
    g = 1 + 9 * sum(state[str(x)] for x in range(30))/30
    return g * round(1- sqrt(state['0']/g))
  def things(i):
    d =dict(T  = Time(),
            f1 = Aux("f1",obj=i.f1,goal=lt),
            f2 = Aux("f2",obj=i.f2,goal=lt))
    for x in xrange(30):
      d[str(x)] =  Aux(str(x),lo=0,hi=1,touch=True)
    return Things(**d)


def sa(f,kmax=1000,era=25,epsilon =0.01,p=0.25,cooling=0.5,seed=1.0):
  rseed(seed)
  def p(old,new,t):
    return e**((new-old)/(t+1))
  things = f().things()
  log = Log(things)			     
  for k in xrange(era): 
     log.another()
  sb,eb = log.another()
  s,e= sb, eb
  for k in xrange(kmax):
    mark="."
    if eb <= epsilon:
      return sb,eb
    sn,en = log.amutant(s,p)
    if en < eb:
      sb,eb = sn,en
      say("!")
    if en < e:
      s,e = sn,en
      mark = "+"
    elif p(e,en,k/kmax**cooling) < r():
      s,e = sn, en
      mark="?"
    say(mark if k % era else ("\n %.3f %s" % (eb,mark)))
  return sb,eb

def _eval1():
  f=Kursawe
  things=f().things()
  log = Log(things)
  for _ in xrange(100): log.another()
  print("========")
  s1,e1 = log.another()
  print(s1);print(e1)
  s2,e2= log.amutant(s1,1)
  print("");print(s2);print(e2,e2/e1)

_eval1()
s,e = sa(Kursawe,kmax=1000,era=25,epsilon =0.01,p=0.33,cooling=0.5,seed=1.0)
print("")
print(e)
