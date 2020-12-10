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

def media_pesada(length,weight):
    mean=length*weight/np.sum(weight)
    return np.sum(mean)

def write_dat_file(encoded, file):
    f = open(file,"wb")
    f.write(bytearray(encoded))
    f.close()

if __name__ == "__main__":
    
    PATH = "D:\\Universidade\\Ano2\\TI\\TP1\\TI---FCTUC\\TP2\\"
    file = "landscape.bmp"
    #egg.bmp, landscape.bmp, pattern.bmp, zebra.bmp

    image = np.array(img.imread(PATH+file))
    image = lzw.deltaRows(image)
    #arr = lzw.deltaColumns(arr)
    #arr = lzw.deltaMean(arr)

    #arr = lzw.deltaFlattenRow(arr)
    #arr = lzw.deltaFlattenColumn(arr)

    encoded, shape_save = lzw.encode(image)
    print(encoded)
    #write_dat_file("testar_lzw.dat", encoded)
    codec = huff.HuffmanCodec.from_data(encoded)
    table = codec.get_code_table()
