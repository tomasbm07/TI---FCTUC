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
	test_target = target[0:len(querry)]
	mutual_info = np.zeros(len(querry), dtype=int)
	tabela = np.shape(len(querry), len(querry))

	for i in range(len(querry)):
		for j in range(len(test_target)):
			

