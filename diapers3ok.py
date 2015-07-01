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

#  ts 5.73933090614 5.73933090614
# ep 22.4757767473 22.4757767473
# early 67.2864581745 67.2864581745
# late 72.9962277924 72.9962277924
# inc 7.0 11.0
# done! 2015-06-29 08:47:45.962529

"""
ts 1.18736297658 1.18736297658
ep 11.6078068745 11.6078068745
early 69.5446699078 69.5446699078
late 73.2893699124 73.2893699124
inc 3.0 4.0
"""
 
@ok
def brooks0():  
  b = BrooksLaw()   
  b.run(10,verbose=True,whatif=dict(ts=6,ep=2,early=67,late=73,inc=20))
   
#@ok
def _brooks1():
  seed(1)
  y = 0 
  out = None
  max = -1
  for x in xrange(104):
    b = BrooksLaw() 
    d1 = b.things().any()
    d1.inc = round(d1.inc)
    d2 = d1.copy()
    while d2.inc <= d1.inc:
      d2.inc = round(d1.inc*3*r())
    v1 = b.run(20,verbose=False ,whatif=d1)
    v2 = b.run(20,verbose=False ,whatif=d2)
    t1 = v1.T
    t2 = v2.T
    if 0.99*t1 <= t2 <= 1.01*t1:
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
  print("")
  for k,v in b.things().things.items():
    if v.touch:
      print(k,d1[k],d2[k])
    
print("done!",now())
   
