from __future__ import print_function,division
from diapers3 import *

#@ok
def _o():
  x=o(a=1,b=2)
  #print(x) 
  x.has().update(dict(c=3,b=5))
  #print(x)
  y = x.copy()
  y.a=10
  assert y.a == 10 and x.a==1
  y["a"] = y["a"] + 100
  assert y.a == 110


#@ok 
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

#ok
def _diapers():
  print(222)
  Diapers().run()

#@ok
def brooks0():
  b = BrooksLaw()
  b.run(5,verbose=True,whatif=dict(inc=10))
   
@ok
def _brooks1():
  seed(1)
  y=0
  out=None
  max = -1
  for x in xrange(1024):
    b = BrooksLaw()
    d1 = b.things().any()
    d1.inc = round(d1.inc)
    d2 = d1.copy()
    d2.inc = round(d1.inc*4*r())
    if d2.inc > d1.inc:
      v1 = b.run(20,verbose=False ,whatif=d1)
      v2 = b.run(20,verbose=False ,whatif=d2)
      t1 = v1.T
      t2 = v2.T
      if 0.9*t1 <= t2 <= 1.1*t1:
        if d2.inc - d1.inc > max:
          max = t2 - t1
          out = (d1,d2)
        y += 1
        say(" ",int(100*y/(x+1)))
      elif t2 > t1:
        print("\n>>",t1,t2,t2/t1)
        for k,v in b.things().things.items():
          if v.touch:
            print(k,d1[k],d2[k])
      else:
        print("!!",t2/t1)      
  d1,d2 = out
  #print("\n>>",t1,t2,t2/t1)
  print("")
  for k,v in b.things().things.items():
    if v.touch:
      print(k,d1[k],d2[k])
    
#    out += [d1]
 # out = sorted(out,key = lambda x: x["r1"])
  #for ts in [ 1,2,4,8]:
   # for ep in [10,20,30]:
    #  for early in [100]:
     #   for inc in [1,2,4,8,10]:
      #    d = dict(early=early,inc=inc,ep=ep,ts=ts)
       #   v = BrooksLaw().run(20,verbose=False,
  #                            whatif=d)
  ###exit()
 # print("")
 # keys = b.things().keys + ["r1"] 
 # def one(s):
  #  return [s[k] for k in keys]
  #lst = [keys] + map(one,out[:10]) + map(one,out[-10:-1])
  #printm(lst)
    
print("done!",now())
   
