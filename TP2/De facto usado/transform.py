import numpy as np

def deltaColumns(info):
    aux = np.roll(info, 1, axis = 0)
    aux[0,:] = 0
    return info - aux

def reverse_deltaColumns(x):
    new = np.array(x, dtype = int)
    for i in range(1,x.shape[0]):
        new[i,:]+=new[i-1,:]
    return new