def val(x): return x.val() if isa(x,Thing) else  x


def add(x,y): return x+y
def sub(x,y): return x-y
def mul(x,y): return x*y
def div(x,y): return x/y
def mod(x,y): return x // y
def pow(x,y): return x**y

  
# amke this the roor of all
class Thing(object):
  def __init__(i,txt,init=100,model=None):
    i.model = model or Model.latest()
    i.txt =txt
    i.model.add(i)
    i.eq = init
  def __repr__(i):
    return "%s=%s" % (i.txt, i.equation)
  def __iadd__(i,eq): i.eq = eq 
  def __add__( i,j): return Eq(i,j,add)
  def __sub__( i,j): return Eq(i,j,sub)
  def __mul__( i,j): return Eq(i,j,mul)
  def __div__( i,j): return Eq(i,j,div)
  def __mod__( i,j): return Eq(i,j,mod)
  def __pow__( i,j): return Eq(i,j,pow)
  def __radd__(i,j): return Eq(j,i,add)
  def __rsub__(i,j): return Eq(j,i,sub)
  def __rmul__(i,j): return Eq(j,i,mul)
  def __rdiv__(i,j): return Eq(j,i,div)
  def __rmod__(i,j): return Eq(j,i,mod)
  def __rpow__(i,j): return Eq(j,i,pow)
  
"""
In my personal opinion this would not be a great
idea in production code: the biggest problem with it
is that it totally non-standard and will probably
leave non-familiar readers wondering where this
novel syntax has suddenly sprung from.
"""
class Model:
  all = []
  @staticmethod
  def latest(): return Model.all[-1]
  def __init__(i,txt,tick=1):
    i.txt,i.tick = txt,tick
    i.t,i.parts,i.all=0,{},{}
  def add(i,p):
    klass          = p.__class__.__name__
    instances      = i.parts.get(klass,{})
    i.all[p.txt]   = instances[p.txt] = p
    i.parts[klass] = instances

@contextmanager
def model(txt,m=None,w=None):
  w = w or o()
  m = m or Model(name)
  Model.all += [m]
  yield m,Stock,Flow,Auxillary,model.tick,o(),o()
  Model.all.pop()

class Eq:
  def __init__(i,l,r,op) :
    i.tree = [op,l,r]
  def __repr__(i):
    op,l,r = i.tree
    return '%s(%s, %s)' % (op.__name__, l, r)
  def val(i) : return i.val1(i.tree,{})
  def val1(i,x,path) :
    assert not id(i) in path, "loop detected"
    path[id(i)] = i
    if isinstance(x,lst):
      op,left,right = lst
      return op(i.val1(left), i.val1(right))
    elif isintance(x,Thing):
      return x.val
    else:
      return x

class Stock(Thing):
  def __init__(i,txt,init=100,model=None):
    super(Stock, self).__init__(txt,init,model)
    i.ins. i.outs = [],[]
  def __iadd__(i,eq):
    _,stock,flow=eq
    i.ins += [(flow,stock)]
  def __isub__(i,eq):
    _,stock,flow=eq
    i.outs = [(flow,stock)]

class Flow(Thing): pass
class Auxillary(Thing): pass
class Par(Auxillary):
  def val(i):
    if 
