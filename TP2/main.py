import random
import time
import numpy as np
import lzw
import alfabeto
import huffman as huff
import matplotlib.image as img
import sys
import scipy.stats as ss

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
    #1MeanRows 2MeanColumns 3FlattenRow 4FlattenColumns
    x1,v1 = np.unique(img, return_counts = True)
    aux = lzw.deltaColumns(img)
    x2,v2 = np.unique(aux, return_counts =True)
    return aux if len(v1)>len(v2) else img

def write_dat_file(encoded, file):
    f = open(file,"wb")
    f.write(bytearray(encoded))
    f.close()

if __name__ == "__main__":
    
    PATH = "D:\\Universidade\\Ano2\\TI\\TP1\\TI---FCTUC\\TP2\\"
    file = "zebra.bmp"
    #egg.bmp, landscape.bmp, pattern.bmp, zebra.bmp

    image = np.array(img.imread(PATH+file))
    #image = transform(image)
    image = lzw.deltaColumns(image)

    #encoded, shape_save = lzw.limited_encode(image)
    encoded, shape_save = lzw.encode(image)

    codec = huff.HuffmanCodec.from_data(encoded)
    table = codec.get_code_table()

    #print(sys.getsizeof(table))

    encoded = huff.encode(encoded, table)
    
    write_dat_file(encoded, file[:-4]+"_ilimited.dat")
    #print(encoded)
    #write_dat_file("testar_lzw.dat", encoded)
    #codec = huff.HuffmanCodec.from_data(encoded)
    #table = codec.get_code_table()
