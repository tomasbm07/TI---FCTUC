import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
import math

PATH = "data\\"


#calc entropia com np.log2
def entropia(valores):
    h=0
    total = np.sum(valores)
    for i in valores:
        h+=-np.log2(i/total)*(i/total)
    return h


# Represents a numpy array in a histogram
def show_histograma(data, istxt, isbmp):
    if istxt:
    	x,values = txt_uniques(data)
    else:
    	x, values = np.unique(data, return_counts=True)
        
    #x,values=group_symbols(data, istxt, isbmp)
    plt.figure(0)
    plt.annotate(f'H = {entropia(values):.2f} bits/pixel', xy=(0, 0), xycoords=('axes fraction', 'figure fraction'),
                 xytext=(65, 5), textcoords='offset points', size=12, ha='right', va='bottom')
    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Repetições")
    plt.bar(x, values, align = "center")
    plt.show()

# Selects how to represent each file type
def histograma(file):
    # Text
    if ".txt" in file:
        file = open(PATH + file, "r")
        text = np.asarray(list(file.read()))
        show_histograma(text,True,False)

    # Images
    if ".bmp" in file:
        image = img.imread(PATH+file)
        # Check se a imagem é RGBA ou Grayscale
        if image.ndim == 2:
            show_histograma(image,False,True)  # Grayscale
        else:
            show_histograma(image[:, :, :1],False,True)  # RGBA, apenas mostra o canal R

            # Sound
    if ".wav" in file:
        sr, sound = wavfile.read(PATH + "saxriff.wav")  # returns Sample Rate and Data
        sound = np.asarray(sound)
        show_histograma(sound[:, :1],False,False) # Apenas mostra o canal esquerdo do som

def get_txt_data(data,group):
    new_data=[]
    i=0
    while (i < len(data)):
        count = 0
        j = i
        aux = ""
        flag = False
        while (count < group):
            if ('a' <= data[j] <= 'z') or ('A' <= data[j] <= 'Z') or ('0' <= data[j] <= '9'):
                aux += str(data[j])
                count += 1
            j += 1
            if (j == len(data)):
                flag = True
                break
        if (flag):
            break
        i = j
        new_data.append(aux)
    return np.asarray(new_data, dtype=str)

#contar apenas letras do alfabeto regulares e digitos
def txt_uniques(data):
    symbols = []
    counts = []
    for i in data:
        if ((i not in symbols) and (('a' <= i <='z') or ('A'<= i <= 'Z'))):
            symbols.append(i)
            counts.append(1)
        elif i in symbols:
            counts[symbols.index(i)] += 1
    return np.asarray(symbols, dtype=str), np.asarray(counts, dtype=int)
    

def get_bmp_data(data,group):
    new_data=[]
    if (data.ndim==2):
        for i in range(len(data)):
            for j in range(0, len(data[i]), group):
                aux = ""
                for k in range(j, j + group):
                    aux += str(data[i, k])
                new_data.append(aux)
    else:
        for i in range(len(data)):
            for j in range(0, len(data[i]), group):
                aux = ""
                for k in range(j, j + group):
                    aux += str(data[i, k, 0])
                new_data.append(aux)
    return np.asarray(new_data, dtype=str)

def get_sound_data(data,group):
    new_data=[]
    for i in range(0,len(data),group):
        aux = ""
        for j in range(i, i + group):
            aux += str(data[j, 0])
            if (j+1==len(data)):
                break
        new_data.append(aux)
    return np.asarray(new_data, dtype=str)


#return simbolos agrupados//contagem deles
def group_symbols(data, istxt,isbmp):
    group=2
    if (istxt):
        new_data=get_txt_data(data,group)
    elif (isbmp):
        new_data=get_bmp_data(data,group)
    else:
        new_data=get_sound_data(data,group)
    x,values=np.unique(new_data,return_counts=True)
    print(x)
    return x, values