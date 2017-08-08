# readlammpstrj.py
# Read lammps trajectory file. Save data in pandas dataframe.

import numpy as np

from snapshot import snapshot
from format_conversion import trj_list2numpy

class RDFConn(object):
    def __init__(self, trjfilename):
        self.trjfn = trjfilename

    #
    # Gnerate DataFrame for everything.
    def genDF(self):
        self.f = open(self.trjfn, 'r+')
        # self.tslist will store timesteps.
        # Each timestep contains the dataframe snapshot.AtomAll for atomic info,
        # snapshot.boxhi, snapshot.boxlo for box info,
        # snapshot.ts for timestep value.
        #
        # Read the trj file
        fbody  = self.f.readlines()
        indx = 0
        # Read trj is stored in a huge list named fbody.
        for line in fbody:
            fbody[indx] = line.split(' ')
            indx += 1
        self.f.close()
        #
        # split the huge list, for every line.
        # separate each time step by while loop.
        indx = 0
        while indx < len(fbody):
            #
            # Do some var type conversion first.

            c_df, ctimestep, cNatom, cboxlo, cboxhi = trj_list2numpy(fbody, indx)
            # Create a snapshot object to store all information for a timestep.
            snap_one = snapshot()
            snap_one.ts = ctimestep
            snap_one.setbox(cboxlo, cboxhi)
            snap_one.AtomAll =  c_df
            snap_one.setbox(cboxlo, cboxhi)
            #
            # Mount the single time step to timestep list self.tslist.
            # Local variable names such as c_df, snap_one, etc will be automatically deleted.
            # Data will not be lost. Stay carm.
            # Python interpreter will handle the data and name ref properly.
            # All data will be callable through the self.tslist and its attributes.

            # Iterate to the next timestep
            indx = indx + cNatom + 9

if __name__ == '__main__':
    go = RDFConn('../input/test0.lammpstrj')
    go.genDF()
