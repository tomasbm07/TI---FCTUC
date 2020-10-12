import numpy as np
import matplotlib.pyplot as plt

#Repesenta um histograma com os valores de x e a sua altura
def show_histograma(data):
    x, values = np.unique(data, return_counts=True)
    plt.figure(0)
    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Repetições")
    plt.bar(x, values, align = "center")
    plt.show()
