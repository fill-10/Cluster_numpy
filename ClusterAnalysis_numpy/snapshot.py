import numpy as np
from pbc_dist import pbc_dist, ifconn
from format_conversion import trj_list2numpy

class snapshot(object):
    def __init__(self):
        self.ts = 0
        self.Natom = 0
        self.AtomAll =  None
    def setbox(self, lowbound, highbound ):
        self.boxlo = lowbound
        self.boxhi = highbound
        self.boxedges = abs(self.boxhi - self.boxlo)

    def selectatoms(self, atomtype):
        self.sel = self.AtomAll[self.AtomAll[:,2]==atomtype,:]
        self.selatomtype = atomtype
        self.Nsel = len(self.sel)
        self.sel = np.hstack(    (    self.sel, np.zeros([self.Nsel, 1], dtype =int)    )  ) # add a column of 
        ###################
        ##################
        np.savetxt(str(self.ts)+'Nsel.txt', np.array([self.Nsel]), fmt = '%10d')

        #################
        #################
        return self.sel
    def findcluster(self, threshold = 1.0):
        # for the sake of speed, always use numpy.array or scipy.array to do the scientific looping calculations!
        # first pointer k scans over all sel atoms as atom1
        for k in range(0,self.Nsel):
            #######################
            #######################
            # monitor progress
            np.savetxt(str(self.ts)+'progress.txt', np.array([k]), fmt = '%10d')
            ################################
            ################################
            
            if self.sel[k,9] <= 0:
                # if k does not belong to any cluster.
                c_cid = max(self.sel[:,9]) +1 # current cid
                clustersize = 0 # flag if k is in cluster. 0 = not in by default. 
                self.sel[k,9] = c_cid
            else:
                # if k belongs to a cluster, read its clusterid
                c_cid = self.sel[k, 9]
                clustersize = 1
            #####################################
            ####################################
            #print c_cid
            ####################################
            ###################################
            #
            # Loop over the atoms below the k.
            n = k+1
            while n < self.Nsel:
                if self.sel[k,9] != self.sel[n,9]:
                    if ifconn(self.sel[ k, 3:6], self.sel[n, 3:6], self.boxedges, threshold):
                        # if k and n are connected.
                        if self.sel[n, 9] <=0:
                            # If n does not belong to any cluster,
                            # assign k's cid to n.
                            self.sel[n, 9 ]  = c_cid
                            clustersize  = 1
                            ##############################
                            #############################
                            #print 'capture new!'
                            #print n
                            ###########################
                            #############################

                        elif self.sel[n,9] >0:
                            s_cid = max([  self.sel[k, 9], self.sel[n, 9]  ] ) #  to select
                            c_cid = min([  self.sel[k, 9], self.sel[n, 9]  ] ) #  to assign
                            ##############################
                            ###############################
                            #print 'combine clusters'
                            #print n
                            #print 's_cid, c_cid'
                            #print s_cid
                            #print c_cid
                            #print 'befor change id'
                            #print self.sel
                            #print 'change done'
                            ###############################
                            ##############################
                            self.sel[self.sel[:,9] == s_cid, 9]= c_cid

                            clustersize  = 1
                
                ######################
                #####################
                #else: print 'skip fast'
                ####################
                ######################

                n += 1
            
            if clustersize <= 0 :
                self.sel[k, 9]= 0
            ##################################
            #################################
            #print 'if in: '+str(clustersize)
            #print ss1.sel
            #################################
            #################################

        return self.sel

    def stats(self):
        (clustersizelist, bins)= np.histogram(   self.sel[:,9],   bins= np.arange(0, max(self.sel[:,9]) + 2 )   )
        # The tricy histogram function, the last bin includes the upper boundary.
        # Can also use bincount instead. But the dtype is object, need to convert astype(int)
        # clusterid =0 indicates the beads not in cluster, i.e. cluster size of 1
        cluster_size_distro =  np.bincount(clustersizelist[1:])[1:] # size of cid=0 makes no sense, skip it. also skip the empty clusterid(s).
        #TODO: HERE IS A BUG. If no cluster formed, clustersize list will be one-element array, e.g. [96]. Then the line above will yield an empty array for the cluster_size_distro, i.e. np.array([]). The next step will cause error because index will be out of range. However, the qchem2 gives back an uninterpretable result for h4/75p. On local desktop, this triggers an error. Need to fix this.
        cluster_size_distro[0] = clustersizelist[0]
        # clusterid 0 indicates the beads in single. add this number to size of 1 "cluser".
        self.clst_distro = np.vstack(  (np.arange(1, len(cluster_size_distro)+1) , cluster_size_distro)   )
        return self.clst_distro

    def updateAtomAll(self):
        self.sel[:,1] = self.sel[:,9] + max(self.AtomAll[:,1])+100000
        self.sel = self.sel[:,:9]
        self.unsel = self.AtomAll[self.AtomAll[:,2]!=self.selatomtype,:]
        self.AtomAll = np.vstack(   (self.unsel, self.sel)   )
        return self.AtomAll
    def saveAtomAll(self):
        # write head:
        f = open(str(self.ts)+'_updated.lammpstrj', 'w')
        np.savetxt(    f, np.array(  [  ['ITEM: TIMESTEP'], [str(self.ts)], ['ITEM: NUMBER OF ATOMS'], [str(self.Natom)],['ITEM: BOX BOUNDS pp pp pp']   ]   ) , fmt= '%s'   )
        f = open(str(self.ts)+'_updated.lammpstrj', 'a')
        np.savetxt(  f, np.vstack(  (self.boxlo, self.boxhi)  ).T , fmt = '%.2f' )
        np.savetxt(  f, np.array(  ['ITEM: ATOMS id mol type x y z ix iy iz']  ) , fmt = '%s' )
        # write atoms
        np.savetxt(  f,  self.AtomAll , fmt = '%8s', delimiter = '  ')

        f.close()


# test
if __name__ == '__main__':
    f = open('../input/test.lammpstrj','r+')
    body = f.readlines()
    indx = 0
    f.close()
    for line in body:
        body[indx] =  line.split(' ')
        indx += 1
    ss1 = snapshot()
    ss1.AtomAll, ss1.ts, ss1.Natom, cboxlo, cboxhi = trj_list2numpy(body, 0)
    ss1.setbox(cboxlo, cboxhi)
    print 'atomall loaded'
    print len(ss1.AtomAll)
    ss1.selectatoms('7')
    print 'total selected:'
    print len(ss1.sel)
    result = ss1.findcluster(1.)
    #np.savetxt(str(ss1.ts)+'snap_out.csv', result, fmt = '%8s', delimiter='\t', header='ITEM: ATOMS id mol type x y z ix iy iz cluster')
    np.savetxt(str(ss1.ts)+'stats.csv',ss1.stats().T, fmt = '%6d')
    ss1.updateAtomAll()
    ss1.saveAtomAll()

