import numpy as np
import matplotlib.pyplot as plt
import math

class lzw_encoder:
    def __init__(self):
        self.n = 0
        self.dic = dict()
        for i in range(-255,256): # caso diferenças
            self.add_symb((i,))

    def add_symb(self, symbol):
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

class lzw_decoder:
    def __init__(self):
        self.next_code = 0
        self.dictionary = dict()
        for i in range(-255,256):
            self.add_to_dictionary((i,))

    def add_to_dictionary(self, symbol):
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

class limited_lzw_encoder:
    def __init__(self):
        self.n = 0
        self.dic = dict()
        self._max_len = 2**16-1
        self._flags = np.zeros(self._max_len-512, dtype = 'int8')
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
        self._max_len = 2**16-1
        self._flags = np.zeros(self._max_len-512, dtype = 'int8')
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
    aux=np.append(np.zeros(1), info[:len(info)-1])
    aux=np.array(aux, dtype=int)
    new_info=info-aux
    return new_info.reshape(shape_Safe)# x, values,

def deltaRows(info):
    aux = np.zeros(info.shape, dtype=int)
    aux[:,1:]=np.array(info[:,:info.shape[1]-1],dtype=int)
    new_info = info.copy()-aux
    return new_info

def deltaFlattenColumn(info):
    t_info = info.transpose()
    shape_Save = t_info.shape
    t_info = t_info.flatten()

    aux = np.append(np.zeros(1), t_info[:len(t_info)-1])
    aux = np.array(aux, dtype=int)

    new_info = t_info-aux
    return new_info.reshape(shape_Save).transpose()


def deltaColumns(info):
    info = info.transpose()
    aux = np.zeros(info.shape, dtype=int)
    aux[:,1:]=np.array(info[:,:info.shape[1]-1],dtype=int)
    new_info = info-aux
    return new_info.transpose()

def deltaMean(info):
    rdelta = delta_row_by_row(info)
    cdelta = delta2_column_by_column(info)
    info[1:,1:] = (rdelta[1:,1:]+cdelta[1:,1:])/2
    return info

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

def reverse_delta(encoded):
    for i in range(1:encode.shape[1]):
        encoded[:,i] += encoded[:,i-1]