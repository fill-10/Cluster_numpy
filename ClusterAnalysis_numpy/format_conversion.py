import numpy as np

# trj_list2df(body) can only convert one timestep list to dataframe.
# If multiple timesteps, it only reads and converts the timestep assigned by the argument ind=0.
# The default value ind= 0 indicates that the function will only extract the first timestep, if ind  is not changed.

def trj_list2numpy(fbody,ind = 0 ):
    timestep = int(fbody[ind+1][0])
    Natom = int(fbody[ind +3][0])
    boxinfo = np.array(fbody[ind+5:ind+8]).astype(float)
    boxlo = boxinfo[:,0]
    boxhi = boxinfo[:,1]
    #########################################
    ########################################
    atoms = np.array(fbody[ind+9: ind+9+Natom],dtype = object)
    atoms[:,0] = atoms[:,0].astype(int)
    atoms[:,1] = atoms[:,1].astype(int)
    atoms[:,3:6] =  atoms[:,3:6].astype(float)
    atoms[:,6:9] = atoms[:,6:9].astype(int)
    
    return atoms[:,:9], timestep, Natom, boxlo, boxhi
    ########################################
    #######################################
    #atoms = np.array(fbody[ind+9: ind+9+Natom])
    #Latomid = atoms[:,0].astype(int)
    #Lmolid  = atoms[:,1].astype(int)
    #Ltype   = atoms[:,2]
    #Lxyz    = atoms[:,3:6].astype(float)
    #Lixyz   = atoms[:,6:9].astype(int)
    #return timestep, Natom, boxlo, boxhi, Latomid, Lmolid, Ltype, Lxyz, Lixyz



# test
if __name__ == '__main__':
    f = open('../input/test.lammpstrj','r+')
    body = f.readlines()
    indx = 0
    f.close()
    for line in body:
        body[indx] =  line.split(' ')
        indx += 1
    zz = trj_list2numpy(body)
    print zz
