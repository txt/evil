from __future__ import division,print_function
from lib import *

def weights(m, tiny=2, 
            x=lambda z,j: z[j],
            y=lambda z  : z[-1],
            missing="?"):
  class Nums():
    def __init__(i,inits=[]):
      i.n = i.mu = i.m2 = 0
      map(i.__add__,inits)
    def span(i) : return i.sd()
    def sd(i) :
      return (max(0.0,i.m2)/(i.n - 1))**0.5    
    def __add__(i,z):
      i.n  += 1;
      delta = z - i.mu;
      i.mu += delta/i.n
      i.m2 += delta*(z - i.mu)
    def __sub__(i,z):
      i.n  -= 1;
      delta = z - i.mu;
      if i.n:
        i.mu -= delta/i.n;
        i.m2 -= delta*(z - i.mu)
      else:
        i.mu = i.m2 = 0
  class Syms():
    def __init__(i,inits=[]):
      i.n, i.cnt = 0, {}
      map(i.__add__,inits)
    def span(i) : return i.ent()
    def ent(i) :
      e=0
      for p in [v/i.n for v in i.cnt.values()
                if v > 0]: e -=  p*log(p,2)
      return e     
    def __add__(i,z):
      i.n  += 1; i.cnt[z]  = i.cnt.get(z,0) + 1
    def __sub__(i,z):
      i.n  -= 1; i.cnt[z] -= 1
      
  def divide(this):
    lst = [t[1] for t in this]
    k   = Nums if isa(lst[0],(float,int)) else Syms
    print("K",k)
    lhs, rhs = k(), k(lst)
    n, least, cut = rhs.n , rhs.span(), None
    for j,t in enumerate(this):
      if lhs.n > tiny and rhs.n > tiny:
        print("ln",lhs.n,"ls",lhs.span(),
              "rh",lhs.n,"rs",rhs.span())
        tmp = lhs.n/n*lhs.span() + rhs.n/n * rhs.span()
        if tmp < least:
           cut,least = j,tmp
      rhs - t[1]
      lhs + t[1]
    return cut,least
  def recurse(this,cuts):
    cut,span = divide(this)
    if cut:
      recurse(this[:cut],cuts)
      recurse(this[cut:],cuts)
    else:
      print("s",span)
      cuts += [o(span=span,
                 n=len(this))]
    return cuts
  def weight(col):
    pairs = sorted((x(row,col),y(row)) for row in m
                    if missing != x(row,col))
    n     = len(pairs)
    print("M",n)
    w     = sum(x.span*x.n/n for x in recurse(pairs,[]))
    return w,col    
  # ---- begin main code for 'featureWeighting' -----
  return sorted(weight(col)
                for col,_ in enumerate(m[0]))
