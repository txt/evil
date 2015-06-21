from __future__ import print_function,division
from dsl import *


b= brooksLaw()
rlist(b.all["softwareDevelopmentRate"].equation.tree)

print("\n",datetime.datetime.now())
