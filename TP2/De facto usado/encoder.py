import numpy as np
import matplotlib.image as img
import dahuffman as huff
import pickle
import lzw
import transform

def write_to_encoded(dictionary, shape, encoded, file):
    f = open(file,"wb")
    pickle.dump(dictionary,f)
    pickle.dump(shape, f)
    pickle.dump(encoded, f)
    f.close()

if __name__ == '__main__':

    PATH = "D:\\Universidade\\Ano2\\TI\\TP1\\TI---FCTUC\\TP2\\"
    file = "landscape.bmp"
    #egg.bmp, landscape.bmp, pattern.bmp, zebra.bmp


    try:
    	image = np.array(img.imread(PATH+file))
    except:
    	print("Erro\n")
    	quit()
    #Delta filter aplicado a cada coluna isoladamente
    transformed = transform.deltaColumns(image)
    del image

    #Comprime com recurso ao algoritmo LZW limitado a 2**13 elementos no dicionario
    encoded, shape_save = lzw.encode(transformed) 
    del transformed

    #Cria uma arvore de huffman com base nas probabilidades dos simbolos de 'encoded'
    codec = huff.HuffmanCodec.from_data(encoded)

    #Comprime 'encoded' em códigos de huffman
    encoded = codec.encode(encoded)

    #Guarda o dicionario de huffman, bem como as dimensões da imagem, e depois o array comprimido
    write_to_encoded( codec.get_code_table(), shape_save, encoded, file[:-4]+".dat")