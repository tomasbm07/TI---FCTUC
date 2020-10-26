import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import math
from main import gerar_alfabeto

PATH = "data\\"

#calc entropia com np.log2
def np_entropia(valores):
    total = np.sum(valores)
    prob = valores[valores>0]/total
    return np.sum(-np.log2(prob)*(prob))

# Represents a numpy array in a histogram
def show_histograma(data):
    #if not istxt:
    #    x, values = np.unique(data, return_counts=True)
    #else:
    #    x,values = txt_uniques(data)
    x,values=group_symbols(data)
    plt.figure(0)
    plt.annotate(f'H = {np_entropia(values):.2f} bits/pixel', xy=(0, 0), xycoords=('axes fraction', 'figure fraction'),
                 xytext=(65, 5), textcoords='offset points', size=12, ha='right', va='bottom')
    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Repetições")
    plt.bar(x, values, align="center")
    plt.show()

# Selects how to represent each file type
def histograma(file):
    # Text
    if ".txt" in file:
        file = open(PATH+file, "r")
        text = np.asarray(list(file.read()))
        show_histograma(text)

    # Images
    if ".bmp" in file:
        image = img.imread(PATH+file)
        # Check se a imagem é RGBA ou Grayscale
        image=np.asarray(image)
        if image.ndim == 2:
            show_histograma(image)  # Grayscale
        else:
            show_histograma(image[:, :, :1])  # RGBA, apenas mostra o canal R

            # Sound
    if ".wav" in file:
        sr, sound = wavfile.read(PATH + "saxriff.wav")  # returns Sample Rate and Data
        sound = np.asarray(sound)
        show_histograma(sound[:, :1]) # Apenas mostra o canal esquerdo do som

def get_txt_data(data,group):
    new_data=[]
    i=0
    while (i < len(data)):
        count = 0
        j = i
        aux = ""
        flag = False
        while (count < group):
            if ('a' <= data[j] <= 'z') or ('A' <= data[j] <= 'Z'):
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
def group_symbols(data):
    data=data.flatten()
    group=2
    new_data=[]
    for i in range(0,int(np.prod(data.shape))-group,group):
    	new_data.append(data[i:i+group])
    new_data=np.asarray(new_data)
    print(new_data)
    return gerar_alfabeto(new_data)

  #flatern na leitura
  #leitura unica
  #melhoramento de operação em todos os dados de array (exemplo: entropia) !entropia check!
  #calcular variancia no 4
  #remover np.uniques//alterar uniques
  #alterar forma de agrupamento no 5
  #colocar todos os simbolos no array