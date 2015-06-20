from __future__ import division
from lib import *

@setting #########################################
def DSL(): return o(
  
) ################################################

def val(x): return x.val() if isa(x,Thing) else  x

class Thing:
  def __add__( i, j)  : return i.val() +  val(j)
  def __sub__( i, j)  : return i.val() -  val(j)
  def __mul__( i, j)  : return i.val() +  val(j)
  def __floordiv(i,j) : return i.val() // val(j)
  def __div__( i, j)  : return i.val() /  val(j)
  def __mod__( i, j)  : return i.val() %  val(j)
  def __pow__( i, j)  : return i.val() ** val(j)
  def __radd__(i, j)  : return j +  i 
  def __rsub__(i, j)  : return j -  i
  def __rmul__(i, j)  : return j *  i
  def __rfloordiv(i,j): return j // i
  def __rdiv__(i, j)  : return j /  i
  def __rmod__(i, j)  : return j // i
  def __rpow__(i, j)  : return j ** i
