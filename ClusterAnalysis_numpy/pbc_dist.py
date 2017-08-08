import numpy as np
#from numpy.linalg import norm

def pbc_dist(coor_1, coor_2, boxedges):
    # boxedges is a 3-dim vector of box size, always positive.
    dv = abs(coor_1 - coor_2)
    dvifpbc = abs(boxedges - dv)
    for i in range(0, boxedges.size):
        dv[i] = min(dv[i], dvifpbc[i])
        #
        # old version is not neat...
        #dv = np.hstack( (dv, np.array( [min(   abs(coor_1[i]-coor_2[i]), boxedge[i] - abs( coor_1[i]-coor_2[i]) )  ] )   ) )
    return norm(dv)

def ifconn(coor_1, coor_2, boxedges, threshold):
    dv = abs(coor_1 - coor_2)
    dvifpbc = abs(boxedges - dv) # Apply pbc, forced.
    #
    # Let's see if any component excess the threshold.
    # For each component of the vector dv:
    boxdim = boxedges.size
    for i in range(0, boxdim):
        # Use pbc to update each component of the vector dv, if needed.
        dv[i] = min(dv[i], dvifpbc[i])
        #
        # If any component of updated dv excesses the threshold,
        # the two beads are out of the same cluster.
        # Then, this function should return False and quit this func. Shortcut done.
        if dv[i]> threshold:
            return False
        ##
    # If no component is out of the range,
    # calculate dot product and compare with threshold**2, faster than norm
    if np.dot(dv,dv) > threshold**2:
        return False
    else:
        return True
#

# to test:
if __name__ == '__main__':
    boxlo = np.array([0.0,0.0,0.0])
    boxhi = np.array([2., 2., 1.])
    boxed = abs(boxhi-boxlo)
    coor1 = np.array([1.9,0.01,0.01])
    coor2 = np.array([0.5,1.5,.2])
    from time import clock
    start = clock()
    for i in range(0,100000):
        so= ifconn( coor1,coor2, boxed, 0.82)
    finish = clock()
    print finish -start
    print so

