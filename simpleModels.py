from  __future__ import print_function, division
from lib import *
from run import *

def testcnl(x):
  def f(x) : return x**2 + 3*x + 1
  def g(x) : return 3*x + 3
  return abs(f(x) - g(x))

print(testcnl(-1.39356))

class CurveAndLine(Function):
  def cells(i):
    return Have(#T  = Time(),
                x  = Aux('x',lo=-4,hi=4,touch=True),
                f = Aux("f",obj=lambda st: testcnl(st.x),
                            goal=lt,lo=-20,hi=20))
  
class ZDT1(Function):
  def f1(i,it):
    return it['0']
  def f2(i,it):
    g = 1 + 9 * sum(it[str(x)] for x in range(30))/30
    return g * round(1- sqrt(it['0']/g))
  def cells(i):
    d =dict(T  = Time(),
            f1 = Aux("f1",obj=i.f1,goal=lt,lo=0,hi=1),
            f2 = Aux("f2",obj=i.f2,goal=lt,lo=0,hi=10))
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
      d["f"+str(x)]= Aux(str(x),lo=0,hi=10, obj = i.fn(x))
    return Have(**d)
#tip: every new model is a big deal. new pony to ride. or, at least, to debug

def boolDom(_,fun,it1,e1,it2,e2):
  return fun.have.boolDom(it1,it2)

def lessEnergy(_,fun,it1,e1,it2,e2):
  return e1 < e2

def contDom(always,fun,it1,e1,it2,e2):
  return fun.have.contDom(always.nums,it1,it2)
 
@setting
def SA(): return o(
    p=0.25,
    cooling=1,
    kmax=1000,
    epsilon=0.01,
    cxt={},
    era=100,
    lives=5,
    better=lessEnergy,
    verbose=False)

def sa(fun,**overrides):
  options  = the.SA
  options += overrides
  return sa1(fun,**the.SA)

def sa1(fun, p=None, cooling=None,
             kmax=None,epsilon=None, cxt=None, era=None, better=None,
             lives=None, verbose=None):    
  def decs()        : return decisions(fun.have,cxt)
  def objs(it)      : return fun.have.objectives(it)
  def log()         : return Haves(fun.have)
  def goodbye(info) : fyi(info); return now
  def fyi(x)        : verbose and say(x)
  def improving()   : return last.above(now,epsilon)
  def baseline()    :
    gen0= [seen(decs())for _ in xrange(era)]
    return era ,gen0
  def seen(it):
    it = objs(it)
    now.add(it,k)
    always.add(it,k)
    e = always.aggregate(it)
    now.seen += [(e,it,k)]
    return k+1,it, e
  k, life, eb = 1, lives, 1e32
  now, always = log(), log()
  k,frontier  = baseline()
  last, now   = now, log()
  #=======================
  def p(old,new,t)  : return e**((new-old)/(t+1))
  def mutant(it)    : return mutate(fun.have,it,cxt,p)
  k,s,e = seen(decs())
  fyi("%4s [%2s] %3s "% (k,life,""))
  while True:
    info = "."
    k,sn,en = seen(mutant(s))
    if en < eb:
      fyi("\033[7m!\033[m")
      sb,eb = sn,en
    if en < e:
      s,e = sn,en 
      info = "+"
    elif p(e,en,(k/kmax)**(1/cooling)) < r():
      s,e = sn, en
      info="?"
    if k % era: 
      fyi(info)
    else: 
      life = lives if improving() else life - 1
      if eb < epsilon: return goodbye("E %.5f" %eb)
      if life < 1    : return goodbye("L")
      if k > kmax    : return goodbye("K")
      fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
      last, now  = now, log() 
  
# acoid repeated calls to cells



def _sa0():
  n = lambda z:z.__name__
  what = ZDT1
  last = results = None
  for opt in [de]:
    for better in [lessEnergy,boolDom,contDom]:
      print("\n %s : %s " % (opt.__name__,better.__name__))
      for seed in [1,2,3,4,5,7,8,9,10]:
        fun = what()
        rseed(seed)
        last    = opt(fun,era=50,epsilon=0.001,better=better,verbose=False)
      #print(last.scores.ntiles())
        for k,v in last.nums.items():
          if k[0] == 'f':
            print("%s-%s-%s-%s" % (n(what),k,n(opt),n(better)))
            for x in v.cache.all: print(" %s" % x)

def _sa1():
  # if i added cxt, worse final scores
   with study('ZDT1',use(SA,lives=29,kmax=10000,era=100,
                         epsilon =0.01,p=0.33,cooling=0.1,
                         verbose=True)):
     rseed(1)
     s,e=sa(ZDT1(),**the.SA)

    
#f (0.1009110604332113, [0.101, 0.621, 1.407, 1.933, 2.904], 3.4072182909724873)
#f (0.025561542674170656, [0.026, 0.515, 1.167, 1.881, 7.625], 7.624727551437976)

def _sa2():
  # if i added cxt, worse final scores
  with study('DTZL',use(SA,lives=9,kmax=10000,era=200,
                        epsilon=0.01,p=0.33,cooling=0.10,
                        verbose=True)):
    rseed(1)
    
    s,e=sa(DTLZ7(),**the.SA)
    print(e)                   

 
@setting
def DE(): return o(
    f=0.5, cr=0.3, pop=10, kmax=10000,
    better=lessEnergy,
    epsilon=0.01, cxt={}, 
    lives=9, verbose=False)

def de(fun,**overrides):
  options  = the.DE
  options += overrides
  return de1(fun,**options)


def de1(fun, f=None, cr=None, pop=None,
             better = None,
             kmax=None, epsilon=None, cxt=None, era=None,
             lives=None, verbose=None):
  def decs()       : return decisions(fun.have,cxt)
  def objs(it)     : return fun.have.objectives(it)
  def log()        : return Haves(fun.have)
  def goodbye(info): fyi(info); return now
  def fyi(x)       : verbose and say(x)
  def improving()  : return last.above(now,epsilon)
  def baseline()   :
    gen0= [seen(decs())for k in xrange(era)]
    return era ,gen0
  def seen(it): 
    it = objs(it)
    now.add(it,k)
    always.add(it,k)
    e  = always.aggregate(it)
    now.seen += [(e,it,k)]
    return k+1, it,e
  k, life, eb = 1, lives, 1e32
  now, always = log(),log()
  k,frontier = baseline()
  last,now= now,log()
  #=======================
  def any1(): _,it,_ = any(frontier); return it
  def mutant(a,b,c):
    return crossover(fun.have,a,b,c,f=f,cr=cr,cxt=cxt)
  fyi("%4s [%2s] %3s "% (k,life,""))
  while True:
    info = "."
    for pos in xrange(len(frontier)):
       info = "."
       _,parent,e = frontier[pos]
       k,child,en = seen(mutant(any1(),any1(),any1()))
       if better(always,fun,child,en,parent,e): 
         info = "+"
         frontier[pos] = k,child,en
       if en < eb:
         eb = en
         info = "\033[7m!\033[m"
    if k % era:
      fyi(info)
    else:
      life = lives if improving() else life - 1
      if eb < epsilon : return goodbye("E %.5fs" % eb)
      if life < 1     : return goodbye("L")
      if k > kmax     : return goodbye("K")
      fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
      last, now  = now, log()


#smeagin


def _de1():
  # if i added cxt, worse final scores
  with study('ZDT1',use(DE,verbose=True)):
    rseed(1)
    e=de(ZDT1(),**the.DE)
    print(e)                   

_sa0()
    
#_sa1()
#_de1()
