from __future__ import print_function,division
from diapers3 import *

@ok
def _o():
  x=o(a=1,b=2)
  print(x) 
  x.has().update(dict(c=3,b=5))
  print(x)
  y = x.copy()
  y.a=10
  assert y.a == 10 and x.a==1
  y["a"] = y["a"] + 100
  assert y.a == 110


@ok 
def _thing():
  z = Thing("zz",init=91.34233,prec=0,step=3)
  a = Thing("aa",init=91.34233,prec=0,step=3)
  assert z.restrain(-10) == 0
  t = Time(hi=32)
  ts = Things(z=z,A=a,T=t)
  assert sorted(ts.init().has().values()) == [0,91.34233,91.34233]
  return ts

def _log():
  ts = _thing()
  log = Log(ts,steps=5)
  for dt,t,u,v in sim(ts,spy=8):
    True

ok
def _diapers():
  print(222)
  Diapers().run()
 
@ok
def _brooks():
  print(100)
  BrooksLaw().run(20)
  
import datetime
print("done!",datetime.datetime.now())
   
