import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import np_entropia
PATH = "data\\"

def huffmanCode(data):
	if '.bmp' in data:
		image = np.asarray(img.imread(PATH + data))
		if image.ndim == 2:
			codec = huff.HuffmanCodec.from_data(image.tobytes())
			symbols, weight = np.unique(image, return_counts=True)  # Grayscale
		else:
			codec = huff.HuffmanCodec.from_data(image[:, :, :1].tobytes())
			symbols2, weight=np.unique(image[:, :, :1], return_counts=True)

	elif '.txt' in data:
		file = open(PATH +data, "r")
		text = np.asarray(list(file.read()))
		codec = huff.HuffmanCodec.from_data(text)
		symbols2, weight = np.unique(text, return_counts=True)
		
	elif ".wav" in data:
		sr, sound = wavfile.read(PATH +data)
		sound = np.asarray(sound)
		codec = huff.HuffmanCodec.from_data(sound[:,:1].tobytes())
		symbols2, weight = np.unique(sound[:, :1], return_counts=True)

	symbols, length = codec.get_code_len()
	print(np.average(length,weights=weight))