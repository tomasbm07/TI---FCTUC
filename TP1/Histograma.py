import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
import math

PATH = "data\\"


# Represents a numpy array in a histogram
def histograma(x, values):
    plt.figure(0)
    plt.annotate(f'H = {entropia(values):.2f} bits/pixel', xy=(0, 0), xycoords=('axes fraction', 'figure fraction'),
                 xytext=(65, 5), textcoords='offset points', size=12, ha='right', va='bottom')
    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Repetições")
    plt.bar(x, values, align = "center")
    plt.show()

#calc entropia com np.log2
def entropia(valores):
    total = np.sum(valores)
    prob = valores[valores>0]/total
    return np.sum(-np.log2(prob)*(prob))

