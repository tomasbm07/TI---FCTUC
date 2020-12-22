import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
import math
import pickle
import huffman as huff
from collections import deque
import sys
import lzma

class limited_lzw_encoder:
    def __init__(self):
        self.n = 0
        self.resets = 0        
        self.dic = dict()
        self._max_len = 2**14
        for i in range(1,16+1):
            self.add_symb((i,))

    def add_symb(self, symbol):
        if len(self.dic)==self._max_len:
            self.resets+=1
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
        for i in range(1,16+1):
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

def binary_rle(x):
	values = deque()
	values.append(x[0,0])
	counter = 1
	for i in range(x.shape[0]):
		for j in range(1,x.shape[1]):
			if x[i,j]==values[-1]:
				counter+=1
			else:
				values.append(counter)
				counter=1
	return values

def gray_transformation(x):
	new_x = x^(x>>1)
	return new_x

def reverse_gray_value(x):
    mask = x
    while (mask):
        mask >>= 1
        x ^= mask
    return x

def reverse_gray_transformation(x):
    func = np.vectorize(reverse_gray_value)
    new = func(x)
    return new

"""------------------- // ----------------------"""

def block_transform(m):
	#Todas as possibilidades de blocos binarios
    dic = {
        ((1,1),(1,1)): 1,

        ((1,1),(1,0)): 2,

        ((1,1),(0,1)): 3,

        ((1,0),(1,1)): 4,

        ((0,1),(1,1)): 5,

        ((1,1),(0,0)): 6,

        ((1,0),(1,0)): 7,

        ((1,0),(0,1)): 8,

        ((0,1),(1,0)): 9,

        ((0,1),(0,1)): 10,

        ((0,0),(1,1)): 11,

        ((1,0),(0,0)): 12,

        ((0,1),(0,0)): 13,

 		((0,0),(1,0)): 14,

         ((0,0),(0,1)): 15,

         ((0,0),(0,0)): 16
    }

    x = m.copy()
    flag_swap = '00' #bit 1 linhas, bit 2 colunas

    if x.shape[0] % 2 != 0:
        x = np.append(x, [x[-1]], axis=0)
        flag_swap = '1' + flag_swap[-1]

    if x.shape[1] % 2 != 0:
        x = np.append(x, x[:, -1:], axis=1)
        flag_swap = flag_swap[0] + '1'

    new = np.zeros((x.shape[0] // 2, x.shape[1] // 2), dtype='ushort')
    for i in range(0, x.shape[0], 2):
        for j in range(0, x.shape[1], 2):
            new[i // 2, j // 2] = dic[ tuple(map(lambda x: (x[0],x[1],), x[i:i + 2, j:j + 2])) ]
    return new, flag_swap

def block_reverse(m, flag):
    #Todas as possibilidades de blocos binarios
    dic = {
        1: ((1,1),(1,1)),

        2 :((1,1),(1,0)),

        3 :((1,1),(0,1)),

        4: ((1,0),(1,1)),

        5: ((0,1),(1,1)),

        6: ((1,1),(0,0)),

        7: ((1,0),(1,0)),

        8: ((1,0),(0,1)),

        9: ((0,1),(1,0)),

        10: ((0,1),(0,1)),

        11: ((0,0),(1,1)),

        12: ((1,0),(0,0)),

        13: ((0,1),(0,0)),

        14: ((0,0),(1,0)),

        15: ((0,0),(0,1)),

        16: ((0,0),(0,0))
    }
    
    new = np.zeros((m.shape[0]*2, m.shape[1]*2), dtype = 'uint16')
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            new[2*i:2*i+2,2*j:2*j+2] = np.array(dic[m[i,j]], dtype = 'uint16')

    if flag[0] == '1':
        new = new[:-1,:]
    if flag[1] == '1':
        new = new[:,:-1]
    return new

def limited_encode(matrix):
    shape = matrix.shape
    encoder = limited_lzw_encoder()
    encoded = np.empty(0, dtype=int)
    for i in range(len(matrix)):
        encoded = np.append(encoded, encoder.encode(matrix[i]))
    return encoded, shape

def limited_decode(matrix, shape):
    decoder = limited_lzw_decoder()
    decoded = np.empty(0, dtype = int)

    while (len(decoded)!=np.prod(shape)):
        row, new_start = decoder.decode(matrix, shape)
        matrix = matrix[new_start:]
        decoded = np.append( decoded, row)

    return decoded.reshape(shape)

def write_dat_file(encoded,flag, file):
    f = open(file,"wb")
    pickle.dump(flag, f)
    pickle.dump(encoded, f)
    f.close()

def append_dat_file(encoded, file):
    f = open(file,"ab")
    pickle.dump(encoded, f)
    f.close()

def read_dat_file(file):
    f = open(file, 'rb')
    encoded = pickle.load(f)
    f.close()
    return encoded

def gray_block_lzma_encode(info, file):
    info = gray_transformation(info)
    shape_save = ( math.ceil( info.shape[0]/2 ), math.ceil( info.shape[1]/2 ) )

    i = 0
    while i < 8:
        encoded = (info&(1<<i))>>i

        encoded, flag = block_transform(encoded)

        encoded = lzma.compress(encoded)

        write_dat_file(encoded, shape_save + (flag,), file) if i==0 else append_dat_file(encoded, file)
        i+=1

def gray_block_lzma_decode(file):

    f = open(file, 'rb')
    shape_flag = pickle.load(f)

    i = 0
    while i < 8:
        partial_decoded = pickle.load(f)

        #print(len(partial_decoded))

        partial_decoded = np.frombuffer( lzma.decompress(partial_decoded), dtype = 'uint16' ).reshape(shape_flag[0], shape_flag[1])

        partial_decoded = block_reverse(partial_decoded, shape_flag[2])

        if i==0:
            decoded = partial_decoded.copy()
        else:
            decoded += (partial_decoded<<i)

        i+=1

    decoded = reverse_gray_transformation(decoded)
    f.close()
    return decoded

def gray_block_lzw_huff_encode(info, file):
    info = gray_transformation(info)
    shape_save = ( math.ceil( info.shape[0]/2 ), math.ceil( info.shape[1]/2 ) )

    i = 0
    while i < 8:
        encoded = (info&(1<<i))>>i

        encoded, flag = block_transform(encoded)

        encoded = lzma.compress(encoded)

        write_dat_file(encoded, shape_save + (flag,), file) if i==0 else append_dat_file(encoded, file)
        i+=1


PATH = "D:\\Universidade\\Ano2\\TI\\tp2-meu\\data\\original\\"
file = "zebra.bmp"
#egg.bmp    landscape.bmp   pattern.bmp    zebra.bmp

arr = np.array(img.imread(PATH+file))
gray_block_lzma_encode(arr, file[:-4]+"_without_block.dat")


#arr2 = gray_block_lzma_decode(file[:-4]+".dat")
#print(np.all(arr==arr2))    