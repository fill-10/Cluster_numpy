#findcluster.py
# This script is to run a single snapshot.

import numpy as np
from snapshot import snapshot
from format_conversion import trj_list2numpy

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
    ss1.findcluster(1.)
    #np.savetxt(str(ss1.ts)+'snap_out.csv', result, fmt = '%8s', delimiter='\t', header='ITEM: ATOMS id mol type x y z ix iy iz cluster')
    np.savetxt(str(ss1.ts)+'stats.csv',ss1.stats().T, fmt = '%6d', delimiter = ',')
    ss1.savesel()
    ss1.saveclusersizelist()
    ss1.saveAtomAll()

