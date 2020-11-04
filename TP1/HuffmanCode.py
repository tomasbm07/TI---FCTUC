import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import entropia
PATH = "data\\"

def kraft_mcmillan(length):
	soma=np.full( len(length), 1/2)**length
	return np.sum(soma)

def variancia(length, media):
	var=(length-media)**2
	return np.sum(var/len(length))

def media_pesada(length,weight):
	mean=length*weight/np.sum(weight)
	return np.sum(mean)

def huffmanCode(info,weight):
	codec = huff.HuffmanCodec.from_data(info)
	symbols, length = codec.get_code_len()
	x,y=np.unique(info,return_counts=True)
	print(entropy(y,base=2))
	print("entropia", entropia(weight))
	print(np.average(length, weights=y))
	print("media", media_pesada(length,weight[weight>0]))
	#print("var", variancia( length, np.average(length) ))
	#print(kraft_mcmillan(length))


	#print(symbols)
	#print(length)
	
	#print(media_pesada(length,weight[weight>0]))
