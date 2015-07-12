from __future__ import print_function, division

from cols import *

def cliffsDelta(lst1,lst2,
                dull = [0.147, # small
                        0.33,  # medium
                        0.474 # large
                        ][0] ): 
  "Returns true if there are more than 'dull' differences"
  m, n = len(lst1), len(lst2)
  lst2 = sorted(lst2)
  j = more = less = 0
  for repeats,x in runs(sorted(lst1)):
    while j <= (n - 1) and lst2[j] <  x: 
      j += 1
    more += j*repeats
    while j <= (n - 1) and lst2[j] == x: 
      j += 1
    less += (n - j)*repeats
  d= (more - less) / (m*n) 
  return abs(d)  > dull
  
def runs(lst):
  "Iterator, chunks repeated values"
  for j,two in enumerate(lst):
    if j == 0:
      one,i = two,0
    if one!=two:
      yield j - i,one
      i = j
    one=two
  yield j - i + 1,two


def fromFile(f=None):
  "utility for reading sample data from disk"
  source=open(f) if f else sys.stdin
  def labels(str):
    if str:
      words = re.split(dash,str)
      for n in range(len(words)):
        m = n + 1
        yield ','.join(words[:m])
  import re
  cache = {} 
  num, space,dash = r'^\+?-?[0-9]', 'r[ \t\r\n]',r'[ \t]*-[ \t]*'
  now=None
  for line in source: 
    line = line.strip()
    if line:
      for word in re.split(space,line):
        if re.match(num,word[0]):
          if now:
            for label in labels(now):
              cache[label] += float(word)
        else:
          for label in labels(word):
            if not label in cache:
              cache[label] = Nums()
          now = word
  print(cache.keys())
  for k,v in cache.items():
    print(k,v.n)
  return cache

fromFile()
