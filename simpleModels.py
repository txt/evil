from  __future__ import print_function, division
from lib import *
from run import *

def testcnl(x):
  def f(x) : return x**2 + 3*x + 1
  def g(x) : return 3*x + 3
  return abs(f(x) - g(x))

class CurveAndLine(Function):
  def cells(i):
    return Have(T  = Time(),
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

def sa(fun,**overrides):
  options = the.SA
  options += overrides
  return sa1(fun,**options)

def sa1(fun, p=None, cooling=None,kmax=None,
            epsilon=None, cxt=None, era=None,
            lives=None, verbose=None,all=None):  
  def p(old,new,t)  : return e**((new-old)/(t+1))
  def decs()        : return decisions(fun.have,cxt)
  def mutant(it)    : return mutate(fun.have,it,cxt,p)
  def objs(it)      : return fun.have.objectives(it)
  def log()         : return Haves(fun.have)
  def goodbye(info) :
    print("L",len(now.seen))
    fyi(info); return now,all
  def fyi(x)        : verbose and say(x)
  def improving()   : return last.above(now,epsilon)
  def baseline()    :
    gen0= [seen(decs(),k)for k in xrange(era)]
    return era ,gen0
  def seen(it,k):
    it = objs(it)
    now.add(it,k)
    all.add(it,k)
    e = all.aggregate(it)
    now.seen += [(e,it,k)]
    return it,e
  #=======================
  eb  = 1e32
  all = all or log()
  now = log()
  k,_ = baseline()
  last, now  = now, log()
  life = lives
  k   += 1
  s,e = sb,eb = seen(decs(),k)
  fyi("%4s [%2s] %.3f "% (k,life,eb))
  while True:
    info = "."
    k += 1
    sn,en = seen(mutant(s),k)
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
      if verbose: say(info)
    else: 
      life = lives if improving() else life - 1
      if eb < epsilon: return goodbye("=")
      if life < 1    : return goodbye("x")
      if k > kmax    : return goodbye("0")
      fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
      last, now  = now, log()
  
# acoid repeated calls to cells
 
def _sa0():
  # if i added cxt, worse final scores
   show(the)
   what = CurveAndLine
   for seed in [1]: #,2,3,4,5,7,8,9,10]:
     fun = what()
     all = None
     for opt in [sa]:
         rseed(seed)
         print("")
         now,all = opt(fun,all=all,era=100,epsilon=0.0001,verbose=True)
         say("\n==> eb %s sb %s k %s\n" % now.best())
         #print(opt.__name__,'seed:',seed,out[0].x,
          #     out[1:])


def _sa1():
  # if i added cxt, worse final scores
   with study('ZDT1',use(SA,lives=29,kmax=10000,era=100,
                         epsilon =0.01,p=0.33,cooling=0.1,
                         verbose=True)):
     rseed(1)
     s,e=sa(ZDT1(),**the.SA)


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
    epsilon=0.01, cxt={}, 
    lives=9, verbose=False)

def de(cells,**overrides):
  options = the.DE
  options += overrides
  return de1(cells,**options)

def de1(cells, f=None, cr=None, pop=None, kmax=None,
            epsilon=None, cxt=None,
            lives=None, verbose=None):
  eb  = 1e32
  def any1(): it,_ = any(all); return it
  def decs()      : return decisions(cells,cxt)
  def mutant()    : return crossover(cells,
                                 any1(),any1(), any1(),
                                 f=f,cr=cr,cxt=cxt)
  def objs(it)    : return cells.objectives(it)
  def improving() :
    return last and last.scores.above(now.scores,epsilon)
  def seen(it): 
    it = objs(it)
    now.add(it)
    score = now.aggregate(it,"de",k)
    now.scores += score
    return it,score
  #=======================
  last, now  = None, Haves(cells)
  life = lives
  k = 0
  bestk = 0
  era =  pop*len(cells.decs)
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
         eb = score
         mark = "\033[7m!\033[m"
         sb,eb,bestk = child,score,k
       if verbose: say(mark)
    if k % era == 0:
      if verbose:
        say("\n[%2s] %.3f %s" % (life,eb,mark))
      life = lives if improving() else life - 1
      last, now  = now, Haves(cells)
  return sb,eb,bestk,k

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
