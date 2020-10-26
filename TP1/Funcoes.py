import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import histograma

PATH = "data\\"


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
	elif ".bmp" in file:
		info = (img.imread(PATH + file))
		x = np.asarray([i for i in range(0, 255 + 1)])
		values = np.zeros(255+1, dtype=int)

		# Check se a imagem é RGBA ou Grayscale
		if info.ndim == 2: # Grayscale
			info=info.flatten()
			for i in info:
				values[x==i] += 1  
		else: # RGBA, apenas mostra o canal R
			info=info[:,:,:1].flatten()
			for i in info:
				values[x==i] += 1

	# Sound
	elif ".wav" in file:
		sr, sound = wavfile.read(PATH + file)  # returns Sample Rate and data
		info = np.asarray(sound)
		x = np.asarray([i for i in range(0, 255 + 1)])
		values = np.zeros(255 + 1, dtype=int)
		info=info[:,:1].flatten()
		for i in info:
			values[x==i] += 1

	else: # informaçao n vem de nehum ficheiro -> gerar alfabeto de input
		
		values=x.zeros
	

	return x, values, info