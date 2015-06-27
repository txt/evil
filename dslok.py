from __future__ import division,print_function
from dsl import *
from cols import *

print(now())
@ok
def things():
  a=Thing("a",10)
  b=Thing("b",20)
  assert   a/b == 0.5
  assert   a*b == 200
  assert   a-b == -10
  assert   a+b == 30
  assert 0.5*a == 5
  assert a*0.5 == 5 
  

@ok
def run():
  for inc in [1,2,4,8,16]:
    n = Nums() 
    for _ in range(16 ):
      b=BrooksLaw()   
      b.about()     
      result = b.start(n=200,report=10,verbose=False,inits=dict(inc=inc))
      n += val(result._t)
    #print({k:val(result[k]) for k in b.goals()})
    n = n.has()
    print(n.median,n.iqr)
      #print('%3s) %8.1f %s' % (t,1*x.d, '*' * int(x.d/250)))

class Log():
  all=[]
  @staticmethod
  def next(model):
    if Log.all:
      i = Log.all[-1]
      j = Log(model)
      for k,old in i.nums:
        new = j.nums[k]
        new.lo, new.hi = old.lo, old.hi
    else:
      Log.all += Log(model)
    return Log.all[-1]
  def gettingWorse(i,j):
    lst = Log.all
    return len(lst) > 1 and \
           and lst[-1].scores < lst[-2].scores
  def __init__(i,model):
    i.model= model
    i.scores  = Nums()
    i.nums = {k:Nums() for k,_ in i.model.goals()}
    Log.all += [i]
  def add(i,xs):
    lst = []
    for k,nums in i.nums():
      x       = xs[k]
      nums   += x
      norm    = nums.norm(x)
      inc     =  1 - norm if v==gt else norm
      lst    += [inc**2]
    score = sqrt(sum(lst))
    i.scores += [score]
    return score

@ok
def de(m,n=32,size=100,npf=10,f=0.5,cf=0.5,delta=1.01):
  def mutate(pop,parent):
    a,b,c,kid = any(pop), any(pop), any(pop),{}
    for k in a:
      x,y,z  = a[k], b[k], c[k]
      kid[k] = x + f(y - z) if cf < r() else x
    k,v     = any(parent.items())
    kid[k]  = v
    return kid
  log    = Log.next(m)
  np     = 10 * len(m.goals())
  pop    = [m.maybe() for _ in xrange(size)]
  scores = [log.add(x) for x in pop]
  yield log,pop
  for _ in xrange(n):
    for i in xrange(size):
      parent  = pop[i]
      score   = scores[i]
      kid     = mutate(pop,parent)
      results = m.start(verbose=False,inits=kid)
      score1  = log.add(results)
      if (score1 - score)/score > delta
        pop[i]    = kid
        scores[i] = score
    yield log,pop

 def watch(m,optimizer):
   Log.all = []
   m = m()
   lives = maxLives = 5
   for log,pop in optimizer(m):
     if Log.gettingWorse()
       lives -= 1
     else:
        lives = maxLives
     if lives < 1:
       break
   return last
     
   
