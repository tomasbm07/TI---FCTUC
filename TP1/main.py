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

	#ft, (ax, ax2) = plt.subplots(2, 1, sharex=True)
	#for i in range(1,8,1):	
	#	print(f"Song0{i}:")
	#	x2, values2, info2 = f.gerar_alfabeto(f"Song0{i}.wav")
	#	im = mt.shazam(info, info2, x, int(0.25*(len(info))))
	#	plt.plot(np.arange(0, len(im), 1), im, label = f"Song0{i}", marker = 'o')
		#ax.plot(np.arange(0, float(f"0.{len(im)}"), 0.1), im, label = f"Song0{i}", marker = 'o')
		#ax2.plot(np.arange(0, float(f"0.{len(im)}"), 0.1), im, label = f"Song0{i}", marker = 'o')

	"""ax2.set_ylim(0.08,0.24)
	ax.set_ylim(0.4, 4)
	ax.spines['bottom'].set_visible(False)
	ax2.spines['top'].set_visible(False)
	ax2.tick_params(labelbottom = False)
	ax.xaxis.tick_top()
	ax.tick_params(labeltop=False)
	ax2.xaxis.tick_bottom()

	#linhas no grafico
	d=.015
	kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
	ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
	ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

	kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
	ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
	ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
	
	ax.legend()
	plt.show()"""



if __name__ == "__main__":
	main()
