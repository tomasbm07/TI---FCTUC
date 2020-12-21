import random
import time
import numpy as np
import lzw
import alfabeto
import huffman as huff
import matplotlib.image as img
import matplotlib.pyplot as plt
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

def write_dat_file(data, file):
    f = open(file,"wb")
    pickle.dump(data,f)
    f.close()

def append_dat_file(data, file):
    f = open(file,"ab")
    pickle.dump(data, f)
    f.close()

def read_dat_file(file):
    f = open(file, 'rb')
    encoded = pickle.load(f)
    f.close()
    return encoded

if __name__ == "__main__":
    
    PATH = "D:\\Universidade\\Ano2\\TI\\TP1\\TI---FCTUC\\TP2\\"
    file = "pattern.bmp"
    #egg.bmp, landscape.bmp, pattern.bmp, zebra.bmp

    """     Abrir imagem    """
    image = np.array(img.imread(PATH+file))

    #Tranformar imagem por filtro Delta aplicado a colunas
    transformed = lzw.deltaColumns(image)

    #codificar com base no algoritmo LZW, com limite de dicionario
    encoded, shape_save = lzw.limited_encode(transformed)

    del transformed

    #Criar tabela de frequencias de huffman
    codec = huff.HuffmanCodec.from_data(encoded)

    #Codificar a fonte em codigos de huffman
    encoded = codec.encode(encoded)
    
    #Escrever para o ficheiro, a fonte comprimida
    write_dat_file(codec.get_code_table(), file[:-4]+".dat")
    append_dat_file(encoded, file[:-4]+".dat")
    #Ler do ficheiro a informação comprimida
    #encoded = read_dat_file(file[:-4]+"_2.dat")

    #Inverter os códigos de huffman
    #decoded = np.array(codec.decode(encoded), dtype = int)

    del codec
    #Descodificar a informação comprimida através do algoritmo lzw
    #decoded = np.array(lzw.decode(decoded, shape_save), dtype='uint8')
    #decoded = np.array(lzw.limited_decode(decoded, shape_save), dtype='uint8')

    #Reverter a transformação aplicada por deltas nas colunsa
    #lzw.reverse_delta(decoded)

    #print(np.all( decoded == image))