import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import math
PATH = "data\\"

#calc entropia com math
def entropia(valores):
    h=0
    total = np.sum(valores)
    for i in valores:
        if i!=0:
            h+=(i/total)*math.log2(1/(i/total))
    return h
#calc entropia com np.log2
def np_entropia(valores):
    h=0
    total = np.sum(valores)
    for i in valores:
        if i!=0:
            h+=-np.log2(i/total)*(i/total)
    return h

#contar apenas letras do alfabeto regulares e digitos
def uniques(data):
    symbols = []
    counts = []
    for i in data:
        if ((i not in symbols) and (('a' <= i <='z') or ('0'<= i <= '9') or ('A'<= i <= 'Z'))):
            symbols.append(i)
            counts.append(1)
        elif i in symbols:
            counts[symbols.index(i)]+=1
    return np.asarray(symbols,dtype=str), np.asarray(counts,dtype=int)


# Represents a numpy array in a histogram
def show_histograma(data,flag):
    if not flag:
        x, values = np.unique(data, return_counts=True)
    else:
        x,values = uniques(data)
    plt.figure(0)
    plt.annotate(f'H = {entropy(values,base=2):.2f} bits/pixel', xy=(0, 0), xycoords=('axes fraction', 'figure fraction'),
                 xytext=(65, 5), textcoords='offset points', size=12, ha='right', va='bottom')
    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Repetições")
    plt.bar(x, values, align="center")
    plt.show()
    print(entropia(values), np_entropia(values), sep='\n')


# Selects how to represent each file type
def histograma(file):
    # Text
    if ".txt" in file:
        file = open(PATH + file, "r")
        text = np.asarray(list(file.read()))
        show_histograma(text,True)

    # Images
    if ".bmp" in file:
        image = img.imread( PATH + file)
        # Check se a imagem é RGBA ou Grayscale
        if image.ndim == 2:
            show_histograma(image,file)  # Grayscale
        else:
            show_histograma(image[:, :, :1],False)  # RGBA, apenas mostra o canal R

    # Sound
    if ".wav" in file:
        sr, sound = wavfile.read(PATH + "saxriff.wav")  # returns Sample Rate and Data
        sound = np.asarray(sound)
        show_histograma(sound[:, :1],False) # Apenas mostra o canal esquerdo do som