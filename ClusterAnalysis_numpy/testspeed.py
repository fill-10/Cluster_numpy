import timeit

import pandas as pd
import scipy as sp
import numpy as np
from numpy import linalg as LA

def test():
    l = [['1','2','3','4','5'],['4','5','6','7','10.0001']]*1000000
    df = pd.DataFrame(l)
    df[0] = df[0].astype(int)
    df[1] = df[1].astype(float)
    df[2] = df[2].astype(float)
    df[3] = df[3].astype(float)

    df[4] = df[4].astype(float)
    dfv = df.values
    hi = len(dfv)
    for i in range(0,hi):
        eta = dfv[i,1:3] - dfv[i,3:5]
        if np.all( abs( eta)<2.5):
            dist = LA.norm(eta)
            if dist < 3.:
                dfv[i, 0] =  11



def test2():
    l = [['1','2','3','4','5'],['4','5','6','7','10.0001']]*1000000
    df = np.array(l)
    alpha = df[:, 0].astype(int)
    beta = df[:, 1:3].astype(float)
    gama = df[:,3:5].astype(float)
    hi = len(beta)

    for i in range(0,hi):
        eta = beta[i]-gama[i]
        if np.all(  abs(eta)<2.5 ):
            dist = LA.norm(eta)
            if dist< 3.:
                alpha[i] = 11

#test()
#test2()


testnumber = 1

print(timeit.timeit( "test()", setup = 'from __main__ import test', number= testnumber ) /testnumber )
print(timeit.timeit( "test2()", setup = 'from __main__ import test2', number= testnumber ) /testnumber )


#NOTE
    # Test results here:
    # Create 100k row 5 col list. converts the data types. pd.DataFrame and .values  =  0.242s, while pure np.array)s = 0.501s.
    
    # 1k row 5 col list, calcuate detal vector eta line by line over for loop. pd.DataFrame (no extract values) and save result in .values =1.935s (keeping result in pd.Series makes no much difference.), while pure np.array)s = 0.00853s. 

    # Create 100k row 5 col list. Convert data types. Calcuate detal vector eta line by line over for loop. pd.DataFrame.values =1.029s, while pure np.array)s = 0.898s.


    # Create 100k row 5 col list. Convert data types. Calcuate detal vector eta line by line over for loop. Check if all coor in threshold. (Half of rows should be.)  pd.DataFrame.values =3.045s, while pure np.array)s = 2.859 s.

    # Create 100k row 5 col list. Convert data types. Calcuate detal vector eta line by line over for loop. Check if all delta vector abs( coor) in threshold. (Half of rows should be.) If in, calculate norm.  pd.DataFrame.values =3.310s, while pure np.array)s = 3.014 s.
    # same as above line except using two np.all)s instead of abs(), 4.67 vs 4.61. Worse....
    # Create 100k row 5 col list. Convert data types. Calcuate detal vector eta line by line over for loop. Check if all delta vector abs( coor) in threshold. (Half of rows should be.) If in, calculate norm. Change id if in the range of threshold, 4.541s vs 4.241s.


#    Each test goes under 10 times of run and averaged ,except for the very slow 1000 ro pandas.DataFrame loop. Run on the vertual box on a windows 10 box. Machine is Dell Precision T3500. CPU Intel Xeon W3530 2.80GHz. total 8 Hyperthread Cores.

    # Additional test: 1000k row 5 col list, calculate norm, change id, etc. All done. Only a 1 time run, 45.076s vs 41.602s.

    # CONCLUSION:
    # Never loop over rows by using pandas.DataFrame itself!!
    # pandas.DataFrame is a little faster in converting data type, while numpy.array cathces up when futher calculating the delta vector and so on. The numpy.array is 10% faster finally. The difference can be in the dfv[i,1:3] in each loop dfv[i,3:5], the locating might be a time consuming factor.
    # In short, pandas has some advantages in dealing with csv and xlsx files, both input and output. But pandas module needs to be installed by user. It is not a default package. If want to run on server, better to avoid pandas and only use numpy. One can use .tofile or .savetxt for io. Some other func such as .unique or something to do the simple stats analysis. Search internet.
