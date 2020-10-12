import numpy as np
import matplotlib.pyplot as plt

#Repesenta um histograma com os valores de x e a sua altura
def show_histograma(x, values):
	plt.figure(0)
	plt.title("Histograma")
	plt.xlabel("Valores")
	plt.ylabel("Repetições")
	plt.bar(x, values, align="center",)
	plt.show()


#Conta as repeticoe no Array
def cria_hist(P):
    p_copy= np.asarray(P)
    hist = np.zeros([p_copy.max() - p_copy.min() + 1], dtype=int)
    for i in p_copy:
        hist[i - p_copy.min()] += 1
    #print(hist)
    return hist


#Cria Array com os valores min e max do argumento
def cria_valores(P):
    p_copy = np.asarray(P, dtype=int)
    valores = np.asarray([i for i in range(p_copy.min(), p_copy.max() + 1)], dtype=int)
    #print(valores)
    return valores
