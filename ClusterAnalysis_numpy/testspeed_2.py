import timeit

import pandas as pd
import scipy as sp
import numpy as np
from numpy import linalg as LA

def test():
    a = np.array([1.,2.,3.])
    b = np.array([2.,2.,2.])
    c = abs(a-b)
    d= LA.norm(c)

def test2():
    a = np.array([1.,2.,3.])
    b = np.array([2.,2.,2.])
    c = abs(a-b)

def test3():
    a = np.array([1.,2.,3.])
    b = np.array([2.,2.,6.])
    c = abs(a-b)
    for i in range(0, len(c)):
        if c[i]>1.:
            pass
def test4():
    a = np.array([1.,2.,3.])
    b = np.array([2.,2.,6.])
    c = abs(a-b)
    if np.amax(c >1., axis = 0):
        pass

def test5():
    b = np.array([1.,0.5,6.])
    for i in range(0, len(b)):
        if b[i]>1.:
            pass
def test6():
    b = np.array([1.,0.5,6.])
    if  np.amax(b >1., axis = 0):
        pass
def test7():
    b = np.array([1.,0.5,6.])
    d= LA.norm(b)

#test()
#test2()


testnumber = 1000

print(timeit.timeit( "test()", setup = 'from __main__ import test', number= testnumber ) /testnumber )
print(timeit.timeit( "test2()", setup = 'from __main__ import test2', number= testnumber ) /testnumber )

print(timeit.timeit( "test3()", setup = 'from __main__ import test3', number= testnumber ) /testnumber )
print(timeit.timeit( "test4()", setup = 'from __main__ import test4', number= testnumber ) /testnumber )

print(timeit.timeit( "test5()", setup = 'from __main__ import test5', number= testnumber ) /testnumber )
print(timeit.timeit( "test6()", setup = 'from __main__ import test6', number= testnumber ) /testnumber )


print(timeit.timeit( "test7()", setup = 'from __main__ import test7', number= testnumber ) /testnumber )



#NOTE
    # Test results here:
#|| 1.43718719482e-05
#|| 5.68699836731e-06
#|| 8.06617736816e-06
#|| 1.46050453186e-05
#|| 3.60012054443e-06
#|| 1.06289386749e-05
#|| 9.32192802429e-06

# Compare test 5 6 7:
# for loop+if is faster than .amax! (1/3 time!)
# .amax is even slower than LA.norm! should never use this for a 3D array.
# LA.norm takes 3 times long as check individual coor.
# Considering the simulation box, no mesh will be generated in the analysis. 
# Lots of the scanned pairs will be far out of the threshold. for+if loop can save nearly 2/3 time compared with LA.norm without check. 
# Therefore, for+if then calculate LA.norm should be the best way.

