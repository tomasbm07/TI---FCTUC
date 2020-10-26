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
def entropia(valores):
    h=0
    total = np.sum(valores)
    for i in valores:
        h+=-np.log2(i/total)*(i/total)
    return h


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