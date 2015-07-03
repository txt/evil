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

def keeper(st,objs,now,always,best):
  st      = objs(st)
  now    += st
  always += st
  score   =  always.score(st)
  if best is not None and score > best:
    now.scores += score
  return st,score
  
def sa(f,kmax=1000,era=25,epsilon =0.01,p=0.25,cooling=0.5,seed=1.0):
  eb = None
  def decs()      : return f.things().decisions()
  def objs(st)    : return f.things().objectives(st)
  def mutant(st)  : return f.things().mutate(st,p)
  def p(old,new,t): return e**((new-old)/(t+1))
  def keep(st)    : return keeper(st,objs,now,always,eb)
  def baseline(n) : [keep(decs()) for _ in xrange(n)]
  def improving() :
    return last and last.scores.above(now.scores,epsilon)
  rseed(seed)
  last, now, always = None, Log(f.things()), Log(f.things())
  x,y = keep(objs(decs()))
  print("yyy",y) ; exit()
  baseline(era)
  s,e = sb,eb = keep(decs())
  lives = maxLives = 5
  k = 0

  print(dict(eb=eb,epsilon=epsilon,lives=lives,k=k,kmax=kmax - era))
  while k < 50 or (eb > epsilon and lives > 0 and k < kmax - era):
    k += 1
    mark(".")
    sn,en = keep(mutate(s))
    if en < eb:
      sb,eb = sn,en
      say("!")
    if en < e:
      s,e = sn,en
      mark = "+"
    elif p(e,en,k/kmax**cooling) < r():
      s,e = sn, en
      mark="?"
    if k % era:
      say(mark)
    else: 
      say("\n %.3f %s" % (eb,mark))
      if k > 1:
        lives = maxLives if improving else lives - 1
      i.last = i.now
      i.now  = Log(f.things())
  return sb,eb

def _sa():
  s,e = sa(Kursawe(),kmax=1000,era=100,epsilon =0.001,p=0.33,cooling=0.75,seed=1)
  print("")
  print(e)

def _eval1():
  f=Kursawe()
  things=f.things()
  log = Log(things)
  for _ in xrange(100): log.another()
  print("========")
  s1,e1 = log.another()
  print(s1);print(e1)
  s2,e2= log.amutant(s1,1)
  print("");print(s2);print(e2,e2/e1)


_eval1()
_sa()
