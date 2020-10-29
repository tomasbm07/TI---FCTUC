import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import histograma

PATH = "data\\"


def shazam(querry, target, alfabeto, step):
	aux_step = 0
	test_target = target[aux_step:len(querry)]
	mutual_info = np.zeros(len(querry), dtype=int)
	tabela = np.zeros(1,dtype=int)
	tabela.shape(len(querry), len(querry))

	for i in range(len(querry)):
		tabela[alfabeto==querry[i], alfabeto==querry[i]]+=1


