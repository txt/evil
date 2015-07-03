from __future__ import division,print_function
from lib import *

@setting #########################################
def COL(): return o(
        cache=256,
        tiny = 1e-32,
        dull = [0.147, # small
                0.33,  # medium
                0.474 # large
              ][0] 
) ################################################

class Cache:
  def __init__(i, init=[], size=None):
    i.n, i.size = 0, size or the.COL.cache
    i.all = []
    i._has = None
    map(i.__iadd__,init)
  def __iadd__(i,x):
    i._has = None
    i.n += 1
    now = len(i.all)
    if now < i.size:
      i.all += [x]
    if r() <= now/i.n:
      i.all[ int(r() * now) ]= x
    return i
  def has(i):
    if not i._has:
      i.all = sorted(i.all)
      p = int(len(i.all)/4)
      print(">>",p,len(i.all))
      i._has = o(all   = i.all,
                 median= i.all[p*2] if i.all else 0, 
                 iqr   = i.all[p*3] - i.all[p] if i.all else 0
                )
    return i._has
  def __ne__(i,j,dull=the.COL.dull):
    lt = gt = 0
    for x in i.all:
      for y in j.all:
        if   x > y : gt +=1
        elif x < y : lt +=1
    tmp = abs(gt - lt) / (len(i.all)*len(j.all))
    return tmp > dull
  def above(i,j,epsilon=1):
    if i != j:
      delta = i.has().median - j.has().median
      if delta > epsilon:
        return True
    return False
  
class Nums:
  def __init__(i,inits=[],txt=""):
    i.n = i.mu = i.m2 = 0
    i.txt = txt
    i.reset()
    map(i.__add__,inits)
  def reset(i):
    i.lo,i.hi,i.cache = 1e32, -1e32,Cache()
  def has(i): return i.cache.has()
  def norm(i,x):
    return (x - i.lo) / (i.hi - i.lo + 1e-32)
  def span(i) : return i.sd()
  def sd(i) :
    return (max(0,i.m2)/(i.n-1))**0.5
  def above(i,j,epsilon=1):
    return i.cache.biggerThan(j,cache.epsilon)
  def any(i):
    return i.lo + (i.hi - i.lo)* r()
  def __add__(i,z):
    i.cache += z
    i.lo  = min(z,i.lo)
    i.hi  = max(z,i.hi)
    i.n  += 1;
    delta = z - i.mu;
    i.mu += delta/i.n
    i.m2 += delta*(z - i.mu)
    return i
  def __sub__(i,z):
    i.reset()
    i.n  -= 1;
    delta = z - i.mu;
    if i.n:
      i.mu -= delta/i.n;
      i.m2 -= delta*(z - i.mu)
    else:
      i.mu = i.m2 = 0
    return i
  
class Syms():
  def __init__(i,inits=[]):
    i.n, i.cnt = 0, {}
    map(i.__add__,inits)
  def span(i) :
    return i.ent()
  def ent(i) :
    e=0
    for p in [v/i.n for v in i.cnt.values()
              if v > 0]:
        e -=  p*log(p,2)
    return e     
  def __add__(i,z):
    i.n  += 1
    i.cnt[z]  = i.cnt.get(z,0) + 1
  def __sub__(i,z):
    if i.n > 2:
      i.n  -= 1
      i.cnt[z] -= 1
