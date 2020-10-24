import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import math
PATH = "data\\"

#calc entropia com math
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
    plt.annotate(f'H = {entropy((values),qk=None,base=2):.2f} bits/pixel', xy=(0, 0), xycoords=('axes fraction', 'figure fraction'),
                 xytext=(65, 5), textcoords='offset points', size=12, ha='right', va='bottom')
    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Repetições")
    plt.bar(x, values, align="center")
    plt.show()

def show_histograma_groups(data):
    x, values = alfabeto(data)
    print(entropy(values,base=2))
    plt.figure(0)
    plt.annotate(f'H = {entropy((values),qk=None,base=2):.2f} bits/pixel', xy=(0, 0), xycoords=('axes fraction', 'figure fraction'),
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
        file = open(file, "r")
        text = np.asarray(list(file.read()))
        #show_histograma(text,True)
        show_histograma_groups(text)
    # Images
    if ".bmp" in file:
        image = img.imread(file)
        # Check se a imagem é RGBA ou Grayscale
        if image.ndim == 2:
            show_histograma(image,file)  # Grayscale
        else:
            show_histograma(image[:, :, :1],False)  # RGBA, apenas mostra o canal R
            #show_histograma_groups(image)

            # Sound
    if ".wav" in file:
        sr, sound = wavfile.read("saxriff.wav")  # returns Sample Rate and Data
        sound = np.asarray(sound)
        show_histograma(sound[:, :1],False) # Apenas mostra o canal esquerdo do som

def alfabeto(data):
    def alfabeto(data):
    new_data = []
    for i in range(len(data)):
        data[i]=str.lower(data[i])
    group=2
    y,counta = np.unique(data,return_counts=True)
    i=0
    while ( i < len(data)):
        count=0
        aux=""
        j=i
        flag=False
        while(count<group):
            if ( 'a'<=data[j]<='z' ) or (  'A'<=data[j]<='Z') or (  '0' <= data[j]<='9'):
                aux+=str(data[j])
                count+=1
            j+=1
            if (j==len(data)):
                flag=True
                break
        if (flag):
            break
        i=j
        new_data.append(aux)
    new_data=np.asarray(new_data,dtype=str)
    for i in new_data:
        print(i)
    x,values=np.unique(new_data, axis=0,return_counts=True)
    print(x)
    print(entropy(counta,base=2))
    return x,values