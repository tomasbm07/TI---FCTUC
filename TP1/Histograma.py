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
def show_histograma(x, values):
    plt.figure(0)
    plt.annotate(f'H = {entropia(values):.2f} bits/pixel', xy=(0, 0), xycoords=('axes fraction', 'figure fraction'),
                 xytext=(65, 5), textcoords='offset points', size=12, ha='right', va='bottom')
    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Repetições")
    plt.bar(x, values, align = "center")
    plt.show()


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