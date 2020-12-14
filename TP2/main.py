import random
import time
import numpy as np
import lzw
import alfabeto
import huffman as huff
import matplotlib.image as img
import sys
import scipy.stats as ss
import pickle

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
    pickle.dump(encoded, f)
    f.close()

def read_file(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        f.close()
        return data

if __name__ == "__main__":
    
    PATH = "E:\\UC\\2020-2021\\1º semestre\\TI---FCTUC\\TP2\\"#"D:\\Universidade\\Ano2\\TI\\TP1\\TI---FCTUC\\TP2\\"
    file = "landscape.bmp"
    #egg.bmp, landscape.bmp, pattern.bmp, zebra.bmp

    image = np.array(img.imread(PATH+file))
    #image = transform(image)
    image = lzw.deltaColumns(image)

    encoded, shape_save = lzw.limited_encode(image)
    #encoded, shape_save = lzw.encode(image)

    codec = huff.HuffmanCodec.from_data(encoded)
    table = codec.get_code_table()

    print(table)


    #encoded = huff.encode(encoded, table)

    write_dat_file(encoded, file[:-4]+".dat")

    encoded2 = read_file(file[:-4]+".dat")
    
    encoded2 = huff.decode(encoded, table)

    print(np.all(encoded==encoded2))

    #decoded = lzw.decode(encoded2, shape_save)
    decoded = lzw.limited_decode(encoded2, shape_save)

    print(  np.all(   decoded==image    )   )

    #lzw.reverse_delta(decoded)

    #print(  np.all(   decoded==image    )   )
    #print(encoded)
    #write_dat_file("testar_lzw.dat", encoded)
    #codec = huff.HuffmanCodec.from_data(encoded)
    #table = codec.get_code_table()
