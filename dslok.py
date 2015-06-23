from __future__ import division,print_function
from dsl import *

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
  b=BrooksLaw()
  b.reset()
  b.run(n=200,report=10)
      #print('%3s) %8.1f %s' % (t,1*x.d, '*' * int(x.d/250)))


#@ok
def run1():
  for x,v in BrooksLaw().run(200): print(v)
