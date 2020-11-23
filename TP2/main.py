import random
import time
import numpy as np
import lzw
import alfabeto
import class_lzw
import class_lz77
import huffman
import ctypes
import pathlib

def alfa(info):
    info = np.array(sorted(info.tolist()), dtype=int)
    values = np.empty(0, dtype=int)
    probs = np.empty(0)
    for i in info:
        if ~np.any(values == i):
            values = np.append(values, i)
            probs = np.append(probs, 1)
        else:
            probs = np.where(values == i, probs + 1, probs)
    return values, probs


def diferencas(info):
    aux = np.append(np.zeros(1), info[:len(info) - 1])
    aux = np.array(aux, dtype=int)
    new_info = info - aux

    x = np.arange(256)
    values = np.zeros(256, dtype=int)
    for i in new_info:
        values[x == i] += 1

    return x, values, new_info


def entropia(valores):
    total = np.sum(valores)
    prob = valores[valores > 0] / total
    return np.sum(-np.log2(prob) * (prob))
def media_pesada(length,weight):
    mean=length*weight/np.sum(weight)
    return np.sum(mean)

random.seed(time.time())

if __name__ == "__main__":
    #arr = np.array([random.randint(0, 255) for i in np.arange(50000)], dtype=str)
    arr = np.array([random.randint(0,255) for i in range(50000)])
