from __future__ import division,print_function
from cols import *

@ok
def _cache():
  seed(1)
  c = Cache(size=20)                             
  for x in xrange(0,10000):
    c += x
  lst = sorted(c.all) 
  assert len(lst) == 20
  assert lst ==  [  1864, 2355, 2573, 4256, 4377,
                    5192, 5689, 5788, 6053, 6925,
                    7046, 7922, 8958, 8978, 9209,
                    9501, 9793, 9843, 9938, 9962]

@ok
def _nums():
  n = Nums([10,20],"love")
  assert n.norm(15) == 0.5
  for x in xrange(10000):
    n += x - 5000
  assert n.lo == -5000
  assert n.hi ==  4999
  assert round(Nums([600,470,170,430,300]).sd(),2) == 164.71
  
  
