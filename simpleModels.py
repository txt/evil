from  __future__ import print_function, division
from lib import *
from run import *
  
class ZDT1(Function):
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

def sa(fun,kmax=10000,era=25,epsilon =0.01,p=0.25,cooling=1,seed=None,lives=5):
  eb = None
  def p(old,new,t): return e**((new-old)/(t+1))
  def objs(st)    : return fun.things().objectives(st)
  def mutant(st)  : return fun.things().mutate(st,p)
  def baseline() :
    for _ in xrange(era): monitored(decs())
  def improving() :
    return last and last.scores.above(now.scores,epsilon)
  def decs() :
    ok=False
    while not ok:
      st = fun.things().decisions()
      ok = fun.ok(st)
    return s
  def scoredRelativeToAllways(st)  :
    always.add(st)
    return always.overall(st)
  def monitored(st): 
    st = objs(st)
    now.add(st)
    score = scoredRelativeToAllways(st)
    if score < eb:
      now.scored1(score)
    return st,score
  #=======================
  rseed(seed) 
  last, now, always = None, Log(fun.things()), Log(fun.things())
  baseline()
  life = lives
  k = 0
  s,e = sb,eb = monitored(decs())
  say("[%2s] %.3f "% (life,eb))
  while eb > epsilon and life > 0 and k < kmax - era:
    k += 1
    mark = "."
    sn,en = monitored(mutant(s))
    if en < eb:
      sb,eb = sn,en
      say("!")
    if en < e:
      s,e = sn,en 
      mark = "+"
    elif p(e,en,(k/kmax)**(1/cooling)) < r():
      s,e = sn, en
      mark="?"
    if k % era: 
      say(mark)
    else: 
      say("\n[%2s] %.3f %s" % (life,eb,mark))
      life = lives if improving() else life - 1
      last, now  = now, Log(fun.things())
  return sb,eb
 
def _sa():
  s,e = sa(ZDT1(),lives=9,kmax=1000,era=100,epsilon =0.01,p=0.25,cooling=0.1,seed=1)
  print("")
  print(e)

def _eval1():
  f = ZDT1()
  things=f.things()
  log = Log(things)
  for _ in xrange(100): log.another()
  print("========")
  s1,e1 = log.another()
  print(s1);print(e1)
  s2,e2= log.amutant(s1,1)
  print("");print(s2);print(e2,e2/e1)


def de(fun,pop=100,np=10,cf=0.33,f=0.5, kmax=10000,era=25,epsilon =0.01,seed=None,lives=5):
  eb = None
  def objs(st)    : return f.things().objectives(st)
  def mutant(st)  : return f.things().interpolate(any(),any(),any())
  def baseline() :
    for _ in xrange(era): monitored(decs())
  def improving() :
    return last and last.scores.above(now.scores,epsilon)
  def decs() : ### how ok needs to be in things
    ok=False
    while not ok:
      st = f.things().decisions()
      ok = f.ok(st)
    return s
  def scoredRelativeToAllways(st)  :
    always.add(st)
    return always.overall(st)
  def monitored(st): 
    st = objs(st)
    now.add(st)
    score = scoredRelativeToAllways(st)
    if score < eb:
      now.scored1(score)
    return st,score
  #=======================
  rseed(seed) 
  last, now, always = None, Log(f.things()), Log(f.things())
  baseline()
  life = lives
  k = 0
  s,e = sb,eb = monitored(decs())
  say("[%2s] %.3f "% (life,eb))
  while eb > epsilon and life > 0 and k < kmax - era:
    k += 1
    mark = "."
    sn,en = monitored(mutant(s))
    if en < eb:
      sb,eb = sn,en
      say("!")
    if en < e:
      s,e = sn,en 
      mark = "+"
    elif p(e,en,(k/kmax)**(1/cooling)) < r():
      s,e = sn, en
      mark="?"
    if k % era: 
      say(mark)
    else: 
      say("\n[%2s] %.3f %s" % (life,eb,mark))
      life = lives if improving() else life - 1
      last, now  = now, Log(f.things())
  return sb,eb

_eval1()
_sa()
