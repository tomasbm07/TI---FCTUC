import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
import dahuffman.huffmancodec as huff
import pickle
import lzw
import transform

def read_dat_file(file):
    f = open(file, 'rb')
    data = pickle.load(f)
    f.close()
    return data

if __name__ == '__main__':

    file = "landscape.dat"
    #egg.dat, landscape.dat, pattern.dat, zebra.dat

    #Abrir o ficheiro de leitura de onde seram feitas multiplas leituras 
    try:
    	f = open(file, 'rb')
    except:
    	print("Erro")
    	quit()
    #Lê o dicionario com os codigos de huffman para descodificar a fonte
    _EOF = huff._EndOfFileSymbol()
    codec = huff.HuffmanCodec( pickle.load(f) )

    #Lê as dimensões da imagem
    shape = pickle.load(f)

    #Lê a imagem comprimida
    encoded = pickle.load(f)

    #Descodifica os códigos de huffman, sendo a informação guardada num array numpy
    encoded = np.array(codec.decode(encoded), dtype = int)

    #Descomprime a compressão de lzw
    decoded = lzw.decode(encoded, shape)
    del encoded

    #Reverte a Transformada
    decoded = transform.reverse_deltaColumns(decoded)

    plt.imsave(file[:-4]+".png", np.array(decoded, dtype = 'uint8'), cmap = 'gray')

