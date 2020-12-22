import numpy as np

class lzw_encoder:
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

class lzw_decoder:
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