import HuffmanCode as huff
from Histograma import histograma
import Funcoes as f
import MutualInformation as mt 
from scipy.stats import entropy
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np


def main():
	#lena.bmp, CT1.bmp, binaria.bmp, saxriff.wav, texto.txt
	#file = "texto.txt"
	#x, values, info = f.gerar_alfabeto(file)
	#print(f"Entropy(normal) = {entropy(values, base=2)}")

	"""Exercicios 1, 2 e 3"""
	#histograma(x, values, file)

	"""Exercicio 4"""
	#huff.huffmanCode(info, values)

	"""Exercicio 5"""
	#f.group_symb(info)

	"""Exercicio 6"""
	im = []
	x, values, info = f.gerar_alfabeto("saxriff.wav") #querry

	#targets: "target01 - repeat.wav", "target02 - repeatNoise.wav"
	target = "target01 - repeat.wav"
	x2, values2, info2 = f.gerar_alfabeto(target) #target
	im = mt.shazam(info, info2, x, int((len(info)/4)))

	sr, data = wavfile.read("data\\"+target)
	plt.plot(np.arange(0, int(len(info2)/sr), (len(info2)/len(im))/sr), im)
	plt.title(f"Evolução Informação mútua em {target}")
	plt.xlabel("Tempo(s)")
	plt.ylabel("Informação Mútua")
	plt.grid()
	plt.show()


if __name__ == "__main__":
	main()
