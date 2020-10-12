import numpy as np
import scipy
import matplotlib.pyplot as plt

def cria_hit(P):
    p_copy= np.asarray(P)
    hist = np.zeros([p_copy.max()-p_copy.min()+1], dtype=int)
    for i in p_copy:
        hist[i-p_copy.min()]+=1
    print(hist)
    return hist

def cria_valores(P):
    p_copy = np.asarray(P)
    valores = np.asarray([i for i in range(p_copy.min(), p_copy.max()+1)])
    print(valores)
    return valores

teste = [8,5,1,1,5,8]
histograma = cria_hit(teste)
values = cria_valores(teste)
