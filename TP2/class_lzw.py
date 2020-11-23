#!/usr/bin/python
import numpy as np
import matplotlib.image as img
import random

class lzw_encoder:
    def __init__(self):
        self.next_code = 0
        self.dictionary = dict()
        #for i in range(0,256): #caso normal
        for i in range(-255,256): # caso diferenças
            self.add_to_dictionary((i,))

    def add_to_dictionary(self, symbol):
        self.dictionary[symbol] = self.next_code
        self.next_code = self.next_code + 1

    def encode(self, arr):
        ret = np.empty(0, dtype=int)
        buffer = tuple()
        for i in range(0, len(arr)):
            c = arr[i]
            if buffer == '' or self.dictionary.get( buffer + (c,) , -1) != -1:
                buffer = buffer + (c,)
            else:
                code = self.dictionary[buffer]
                self.add_to_dictionary(buffer + (c,) )
                buffer = (c,)
                ret = np.append(ret, [code])
        if buffer:
            ret = np.append(ret, [self.dictionary[buffer]])

        return ret

class lzw_decoder:
    def __init__(self):
        self.next_code = 0
        self.dictionary = dict()
        for i in range(0,255):
            self.add_to_dictionary(str(i))
    def add_to_dictionary(self, str):
        self.dictionary[self.next_code] = str
        self.next_code = self.next_code + 1
    def decode(self, symbols):
        last_symbol = symbols[0]
        ret = np.array([self.dictionary[last_symbol]])
        for symbol in symbols[1:]:
            if self.dictionary.get(symbol, -1)!=-1:
                current = self.dictionary[symbol]
                previous = self.dictionary[last_symbol]
                to_add = current[0]
                self.add_to_dictionary(previous + to_add) #"""problema = 'simbolo anteior' = nr anterior e nao unidade"""
                ret = np.append(ret, current)
            else:
                previous = self.dictionary[last_symbol]
                to_add = previous[0]
                self.add_to_dictionary(previous + to_add)
                ret=np.append(ret,(previous + to_add))
            last_symbol = symbol
        return ret

def entropia(valores):
    total = np.sum(valores)
    prob = valores[valores > 0] / total
    return np.sum(-np.log2(prob) * (prob))

def diferencas(info):
    shape_Safe=info.shape
    info = info.flatten()
    aux=np.append(np.zeros(1), info[:len(info)-1])
    aux=np.array(aux, dtype=int)
    new_info=info-aux
    """
	x = np.arange(-255,256)
	values = np.zeros(255*2+1, dtype=int)
	for i in new_info:
		values[x==i] += 1
	"""
    return new_info.reshape(shape_Safe)# x, values,

if __name__=='__main__':
    #arr = np.array([ random.randint( 0 , 255) for i in range( 500000 ) ])
    #egg.bmp    landscape.bmp   patterns.bmp    zebra.bmp
    arr = (img.imread("egg.bmp"))
    #arr = diferencas(arr)
    encoder = lzw_encoder()
    encoded = np.empty(arr.shape, dtype=int)
    for i in arr:
        encoded = np.append(encoded, encoder.encode(i))
    print(len(encoded[0]), len(arr[0]))
    x1,v1 = np.unique(arr, return_counts=True)
    x2, v2 = np.unique(encoded, return_counts=True)
    print(entropia(v1), entropia(v2))