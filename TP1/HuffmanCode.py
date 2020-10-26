import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import entropia
PATH = "data\\"

def media(length,weight):
	mean=length*weight/np.sum(weight)
	return np.sum(mean)

def huffmanCode(data,weight):
	codec = huff.HuffmanCodec.from_data(data)
	symbols, length = codec.get_code_len()
	print(np.average(length,weights=weight[weight>0]))
	print(media(length,weight[weight>0]))
