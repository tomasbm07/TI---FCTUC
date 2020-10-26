import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff

PATH = "data\\"


def main():
	# Exercicios 1, 2 e 3
	# lena.bmp, CT1.bmp, binaria.bmp, saxriff.wav, texto.txt
	#histograma("binaria.bmp")

	#huff.huffmanCode("lena.bmp")
	gerar_alfabeto("saxriff.wav")
	


def gerar_alfabeto(file):
	# Text
	if ".txt" in file:
		file = open(PATH + file, "r")
		text = np.asarray(list(file.read()))

		x = [chr(i) for i in range(ord('a'), ord('z') + 1)]
		x += [chr(i) for i in range(ord('A'), ord('Z') + 1)]
		x = np.asarray(x)
		values = np.zeros(52, dtype=int)

		for i in text:
			values[x==i] += 1

		return x, values

	# Images
	if ".bmp" in file:
		image = (img.imread(PATH + file))
		x = np.asarray([i for i in range(0, 255 + 1)])
		values = np.zeros(255+1, dtype=int)

		# Check se a imagem é RGBA ou Grayscale
		if image.ndim == 2: # Grayscale
			for i in image.flatten():
				values[x==i] += 1  
		else: # RGBA, apenas mostra o canal R
			for i in image[:,:,:1].flatten():
				values[x==i] += 1

		return x, values  

	# Sound
	if ".wav" in file:
		sr, sound = wavfile.read(PATH + file)  # returns Sample Rate and data
		sound = np.asarray(sound)
		x = np.asarray([i for i in range(0, 255 + 1)])
		values = np.zeros(255 + 1, dtype=int)

		for i in sound[:,:1].flatten():
			values[x==i] += 1

		return x, values



if __name__ == "__main__":
    main()
