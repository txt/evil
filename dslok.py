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

@ok
def de(n=10,m=BrooksLaw,size=100,npf=10,f=0.5,cf=0.5):
  m=m()
  np = 10 * len(m.goals())
  pop = [m.maybe() for _ in xrange(size)]
  for _ in xrange(n):
    for i,parent in enumerate(pop):
      a,b,c,kid = any(pop), any(pop), any(pop),{}
      for k in a:
        x,y,z = a[k], b[k], c[k]
        old[k] = k,x
        kid[k] = x + f(y - z) if cf < r() else x
      k,v = any(old.values)
      kid[k] = v
      for state in m.start(verbose=False,inits=kid): True
    yield pop

 def watch(m,opt):
   for pop in opt():
     
   
