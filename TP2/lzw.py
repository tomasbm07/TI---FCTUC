import numpy as np
import matplotlib.pyplot as plt
import math

class limited_lzw_encoder:
    def __init__(self):
        self.n = 0
        self.dic = dict()
        self._max_len = 2**13
        for i in range(-255,256): # caso diferenças
            self.add_symb((i,))

    def add_symb(self, symbol):
        if len(self.dic)==self._max_len:
            self.n=0
            self.dic.clear()
            for i in range(-255,256):
                self.add_symb((i,))
        self.dic[symbol] = self.n
        self.n += 1

    def encode(self, arr):
        encoded = np.empty(0, dtype=int)
        buffer = tuple()
        for i in range(0, len(arr)):
            c = arr[i]
            if buffer == '' or self.dic.get( buffer + (c,) , -1) != -1:
                buffer = buffer + (c,)
            else:
                code = self.dic[buffer]
                self.add_symb(buffer + (c,) )
                buffer = (c,)
                encoded = np.append(encoded, [code])
        if buffer:
            encoded = np.append(encoded, [self.dic[buffer]])

        return encoded

class limited_lzw_decoder:
    def __init__(self):
        self.next_code = 0
        self.dictionary = dict()
        self._max_len = 2**13
        for i in range(-255,256):
            self.add_to_dictionary((i,))

    def add_to_dictionary(self, symbol):
        if len(self.dictionary)==self._max_len:
            self.next_code=0
            self.dictionary.clear()
            for i in range(-255,256):
                self.add_to_dictionary((i,))
        self.dictionary[self.next_code] = symbol
        self.next_code = self.next_code + 1

    def decode(self, symbols, shape):
        last_symbol = symbols[0]
        ret = np.array([self.dictionary[last_symbol]])

        n = 1
        while len(ret)< shape[1]:
            if self.dictionary.get(symbols[n], -1)!=-1:
                current = self.dictionary[ symbols[n] ]
                previous = self.dictionary[ last_symbol ]
                to_add = current[0]
                self.add_to_dictionary( previous + (to_add,) )
                ret = np.append(ret, current)

            else:
                previous = self.dictionary[last_symbol]
                to_add = previous[0]
                self.add_to_dictionary(previous + (to_add,))
                ret=np.append( ret,( previous + (to_add,) ) )
            last_symbol = symbols[n]
            n+=1
        return ret, n

def entropia(valores):
    total = np.sum(valores)
    prob = valores[valores > 0] / total
    return np.sum(-np.log2(prob) * (prob))

def deltaFlattenRow(info):
    shape_Safe=info.shape
    info = info.flatten()
    
    aux = np.roll(info, 1)
    aux[0]=0
    return (info-aux).reshape(shape_Safe)

def deltaRows(info):
    aux = np.roll(info, 1, axis = 1)
    aux[:,0] = 0
    return info - aux

def deltaColumns(info):
    aux = np.roll(info, 1, axis = 0)
    aux[0] = 0
    return info - aux

def modular_delta(info):
    new = np.zeros(info.shape, dtype = 'int8')
    new[0,:] = info[0,:]
    flags = []
    for i in range(1,info.shape[0]):
        x1,v1 = np.unique(  info[i], return_counts=True)
        x2,v2 = np.unique(  deltaFlattenRow(info[i]), return_counts=True)
        x3,v3 = np.unique(  deltaColumns( info[i-1:i+1] )[1] , return_counts = True )

        e1 = entropia(v1)
        e2 = entropia(v2)
        e3 = entropia(v3)

        if e3>e2 and e3>e1:
            new[i] = deltaColumns( info[i-1:i+1] )[1]
            flags.append(1)
        elif e2>=e3 and e2 >= e1:
            new[i] = deltaFlattenRow(info[i])
            flags.append(2)
        else:
            new[i] = info[i]
            flags.append(3)
    return new, flags

def encode(matrix):
    shape = matrix.shape
    encoder = lzw_encoder()
    encoded = np.empty(0, dtype=int)
    for i in range(len(matrix)):
        encoded = np.append(encoded, encoder.encode(matrix[i]))
    return encoded, shape

def decode(array, shape):
    decoder = lzw_decoder()
    decoded = np.empty(0, dtype = int)

    while (len(decoded)!=np.prod(shape)):
        row, new_start = decoder.decode(array, shape)
        array = array[new_start:]
        decoded = np.append( decoded, row)

    return decoded.reshape(shape)

def limited_encode(matrix):
    shape = matrix.shape
    encoder = limited_lzw_encoder()
    encoded = np.empty(0, dtype=int)
    for i in range(len(matrix)):
        encoded = np.append(encoded, encoder.encode(matrix[i]))
    return encoded, shape


def limited_decode(array, shape):
    decoder = limited_lzw_decoder()
    decoded = np.empty(0, dtype = int)

    while (len(decoded)!=np.prod(shape)):
        row, new_start = decoder.decode(array, shape)
        array = array[new_start:]
        decoded = np.append( decoded, row)

    return decoded.reshape(shape)

def reverse_delta(x):
    for i in range(1,x.shape[0]):
        x[i,:]+=x[i-1,:]