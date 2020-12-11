import random
import time
import numpy as np
import lzw
import alfabeto
import huffman as huff
import matplotlib.image as img

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

def transform(img):
    entropys = [0 for i in range(5)]
    for i in range(5):
        pass

def write_dat_file(encoded, file):
    f = open(file,"wb")
    f.write(bytearray(encoded))
    f.close()

if __name__ == "__main__":
    
    PATH = "D:\\Universidade\\Ano2\\TI\\TP1\\TI---FCTUC\\TP2\\"
    file = "pattern.bmp"
    #egg.bmp, landscape.bmp, pattern.bmp, zebra.bmp

    image = np.array(img.imread(PATH+file))
    #image = transform(image)
    image = lzw.deltaRows(image)
    #arr = lzw.deltaColumns(image)
    #arr = lzw.deltaMean(image)

    #arr = lzw.deltaFlattenRow(arr)
    #arr = lzw.deltaFlattenColumn(arr)

    encoded, shape_save = lzw.limited_encode(image)
    #encoded, shape_save = lzw.encode(image)

    codec = huff.HuffmanCodec.from_data(encoded)
    table = codec.get_code_table()

    encoded = huff.encode(encoded, table)
    
    write_dat_file(encoded, "teste.dat")
    #print(encoded)
    #write_dat_file("testar_lzw.dat", encoded)
    #codec = huff.HuffmanCodec.from_data(encoded)
    #table = codec.get_code_table()
