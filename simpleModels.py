from  __future__ import print_function, division
from lib import *
from run import *

class Kursawe(Function):
  def f1(i,state):
    print("F1")
    return state['0']
  def f2(i,state):
    print("F2")
    g = 1 + 9 * sum(state[str(x)] for x in range(30))/30
    return g *round(1- sqrt(state['0']/g))
  def things(i):
    d =dict(T  = Time(),
            f1 = Aux("f1",obj=i.f1,goal=lt),
            f2 = Aux("f2",obj=i.f2,goal=lt))
    for x in xrange(30):
      d[str(x)] =  Aux(str(x),lo=0,hi=1,touch=True)
    return Things(**d)

#t = Kursawe().things()
#for _ in range(10000): 
#  t.evaluate(t.any())

def sa(f,kmax=10,era=100,epsilon =0.05,p=1):
  def p(old,new,t):
    print(old,new,t)
    return e**((new-old)/(t+1))
  things = f().things()
  log = Log(things)			     
  for k in xrange(era): 
     log.another()
  sb,eb = log.another()
  eb = 1 - eb
  s,e= sb, eb
  for k in xrange(kmax):
    mark="."
    if e <= epsilon:
      return eb,sb
    sn,en = log.amutant(s)
    en = 1 - en
    if (en == eb): print("?")
    if en < eb:
      sb,eb = sn,en
      mark="!"
    if en < e:
      s,e = sn,en
      mark="+"
    elif p(e,en,k/kmax) < r():
      s,e = sn, en
      mark="?"
    say(mark if k % era else ("\n %.3f %s" % (eb,mark)))
    
sa(Kursawe)
