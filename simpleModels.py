from  __future__ import print_function, division
from lib import *
from run import *

@setting
def SA(): return o(
    p=0.25,
    cooling=1,
    kmax=1000,
    epsilon=0.01,
    cxt={},
    era=100,
    lives=5,
    verbose=False)
           
class ZDT1(Function):
  def f1(i,it):
    return it['0']
  def f2(i,it):
    g = 1 + 9 * sum(it[str(x)] for x in range(30))/30
    return g * round(1- sqrt(it['0']/g))
  def cells(i):
    d =dict(T  = Time(),
            f1 = Aux("f1",obj=i.f1,goal=lt),
            f2 = Aux("f2",obj=i.f2,goal=lt))
    for x in xrange(30):
      d[str(x)] =  Aux(str(x),lo=0,hi=1,touch=True)
    return Have(**d)

class DTLZ7(Function):
  "Has M-1 disconnected regions"
  def s(i,it,n): return it[str(n)]
    
  def __init__(i,m=20):
    i.m = m # which w eill process as 0 ... i.m - 1
  def g(i,it):
    return  1 + 9/i.m * sum(i.s(it,x) for x in xrange(0,i.m))
  def h(i,it,g):
    return i.m - sum([i.s(it,x)/(1+g)*(1+sin(3*pi*i.s(it,x)))
                      for x in xrange(0,i.m - 1)])
  def fn(i,n):
    return lambda it:i.f(n,it)
  def f(i,n,it):
    if n < (i.m - 2) :
      return i.s(it,n)
    else:
      g = i.g(it,)
      h = i.h(it,g)
      return (1 + g)*h
  def cells(i):
    d = dict(T=Time())
    for x in xrange(i.m):
      d[    str(x)]= Aux(str(x),lo=0,hi=1, touch=True)
      d["f"+str(x)]= Aux(str(x),lo=0,hi=1, obj = i.fn(x))
    return Have(**d)
#tip: every new model is a big deal. new pony to ride. or, at least, to debug


def sa(fun, p=None, cooling=None,kmax=None,
            epsilon=None, cxt=None, era=None,
            lives=None, verbose=None):
  eb = None
  def p(old,new,t): return e**((new-old)/(t+1))
  def decs()      : return decisions(fun.cells(),cxt)
  def mutant(it)  : return mutate(fun.cells(),it,cxt,p)
  def objs(it)    : return fun.cells().objectives(it)
  def baseline()  : [ seen(decs()) for _ in xrange(era) ]
  def improving() :
    return last and last.scores.above(now.scores,epsilon)
  def seen(it): 
    it = objs(it)
    now.add(it)
    always.add(it)
    score = always.aggregate(it)
    if score < eb:
      now.scores += score
    return it,score
  #=======================
  last, now, always = None, Haves(fun.cells()), Haves(fun.cells())
  print("era",era)
  baseline()
  life = lives
  k = 0
  s,e = sb,eb = seen(decs())
  if verbose: say("[%2s] %.3f "% (life,eb))
  while True:
    if eb < epsilon  : verbose and say("="); break
    if life < 1      : verbose and say("x"); break
    if k > kmax - era: verbose and say("0"); break
    k += 1
    mark = "."
    sn,en = seen(mutant(s))
    if en < eb:
      sb,eb = sn,en
      if verbose: say("\033[7m!\033[m")
    if en < e:
      s,e = sn,en 
      mark = "+"
    elif p(e,en,(k/kmax)**(1/cooling)) < r():
      s,e = sn, en
      mark="?"
    if k % era: 
      if verbose: say(mark)
    else: 
      if verbose:
        say("\n[%2s] %.3f %s" % (life,eb,mark))
      life = lives if improving() else life - 1
      last, now  = now, Haves(fun.cells())
  if verbose:
    print("\n");print(dict(eb=eb,life=life,k=k))
  return sb,eb
 
def _sa1():
  # if i added cxt, worse final scores
   with study('ZDT1',use(SA,lives=9,kmax=1000,era=100,
                         epsilon =0.01,p=0.33,cooling=0.1,
                         verbose=True)):
     s,e=sa(ZDT1(),**the.SA)
     print("")
     print(e)

_sa1()

def _sa2():
  # if i added cxt, worse final scores
  with study('DTZL',use(SA,lives=9,kmax=10000,era=200,
                        epsilon=0.01,p=0.33,cooling=0.10,
                        verbose=True)):
    s,e=sa(DTLZ7(),**the.SA)
    print(e)                   

#_sa2()

@setting
def DE(): return o(
    f=0.5, cr=0.3, pop=10, kmax=1000,
    epsilon=0.01, cxt={}, 
    lives=5, verbose=False)

def de(fun, f=None, cr=None, pop=None, kmax=None,
            epsilon=None, cxt=None,
            lives=None, verbose=None):
  eb  = 1e32
  def any1(): it,_ = any(all); return it
  def decs()      : return decisions(fun.cells(),cxt)
  def mutant()    : return crossover(fun.cells(),
                                 any1(),any1(), any1(),
                                 f=f,cr=cr,cxt=cxt)
  def objs(it)    : return fun.cells().objectives(it)
  def improving() :
    return last and last.scores.above(now.scores,epsilon)
  def seen(it): 
    it = objs(it)
    now.add(it)
    always.add(it)
    score = always.aggregate(it)
    now.scores += score
    return it,score
  #=======================
  last, now, always  = None, Haves(fun.cells()), Haves(fun.cells())
  life = lives
  k = 0
  era =  pop*len(fun.cells().decs)
  all = [seen(decs()) for _ in xrange(era)]
  while True:
    if eb < epsilon  : verbose and say("="); break
    if life < 1      : verbose and say("x"); break
    if k > kmax - era: verbose and say("0"); break
    mark = "."
    for pos in xrange(era):
       mark = "."
       parent,score0 = all[pos]
       child,score = seen(mutant())
       k += 1
       if (score < score0):
         mark = "+"
         all[pos] = child,score
       if score < eb:
         mark = "\033[7m!\033[m"
         eb = score
       if verbose: say(mark)
    if k % era == 0:
      if verbose:
        say("\n[%2s] %.3f %s" % (life,eb,mark))
      life = lives if improving() else life - 1
      last, now  = now, Haves(fun.cells())
  if verbose:
    print("\n");print(dict(eb=eb,life=life,k=k))
  return eb

#smeagin


def _de1():
  # if i added cxt, worse final scores
  with study('ZDT1',use(DE,verbose=True)):
    e=de(ZDT1(),**the.DE)
    print(e)                   

_de1()
