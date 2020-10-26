import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import HuffmanCode as huff
from Histograma import histograma,group_symbols

PATH = "data\\"


def main():
	# Exercicios 1, 2 e 3
	# lena.bmp, CT1.bmp, binaria.bmp, saxriff.wav, texto.txt
	symbols,counts,informacao=gerar_alfabeto("CT1.bmp")

	#histograma(symbols,counts)
	group_symbols(informacao)
	#huff.huffmanCode(informacao,counts)
	
	


def gerar_alfabeto(file):
	# Text
	if ".txt" in file:
		file = open(PATH + file, "r")
		info = np.asarray(list(file.read()))

		x = [chr(i) for i in range(ord('a'), ord('z') + 1)]
		x += [chr(i) for i in range(ord('A'), ord('Z') + 1)]
		x = np.asarray(x)
		values = np.zeros(52, dtype=int)

		for i in info:
			values[x==i] += 1

	# Images
	if ".bmp" in file:
		info = (img.imread(PATH + file))
		x = np.asarray([i for i in range(0, 255 + 1)])
		values = np.zeros(255+1, dtype=int)

		# Check se a imagem é RGBA ou Grayscale
		if info.ndim == 2: # Grayscale
			info=info.flatten()
			for i in info.flatten():
				values[x==i] += 1  
		else: # RGBA, apenas mostra o canal R
			info=info[:,:,:1].flatten()
			for i in info:
				values[x==i] += 1

	# Sound
	if ".wav" in file:
		sr, info = wavfile.read(PATH + file)  # returns Sample Rate and data
		info = np.asarray(sound)
		x = np.asarray([i for i in range(0, 255 + 1)])
		values = np.zeros(255 + 1, dtype=int)
		info=info[:,:1].flatten()
		for i in info:
			values[x==i] += 1

	return x, values, info



if __name__ == "__main__":
    main()
