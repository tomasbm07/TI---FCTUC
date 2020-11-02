import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import histograma
from pyitlib import discrete_random_variable as drv

PATH = "data\\"


def shazam(querry, target, alfabeto, step):
	mutual_info = np.zeros(len(target) - len(querry) + 1, dtype=float)
	tabela = np.zeros( ( len( alfabeto ), len( alfabeto ) ), dtype=float)
	index = 0
	for j in range(0,len(target)-len(querry)+1,step):
		#Set the test_target 
		test_target = target[j:j + len(querry)+1] 

		#if len(test_target)<len(querry):
		#	break

		#Set the repetitions values
		for i in range( len(querry) ):
			tabela[ alfabeto==test_target[i], alfabeto==querry[i] ]+=1

		#Probabilidades
		tabela[tabela>0] /= len(querry)

		#Calculate Mutual Information
		for x in alfabeto:

			for y in alfabeto:

				if tabela[ x, y ] != 0:
					mutual_info[index] += ((tabela[x, y]/tabela.sum()) * (np.log2( (tabela.sum()*tabela[x,y]) / ( (tabela.sum(axis=1)[x])*(tabela.sum(axis=0)[y]) ) )))

		index += 1
		tabela = np.zeros((len(alfabeto), len(alfabeto)), dtype=float)

	print(mutual_info, len(mutual_info))



querry = np.asarray([2, 6 ,4 ,10 ,5, 9, 5 ,8, 0, 8], dtype=int)
target = np.asarray([6,8,9,7,2,4,9,9,4,9,1,4,8,0,1,2,2,6,3,2,0,7,4,9,5,4,8,5,2,7,8,0,7,4,8,5,7,4,3,2,2,7,3,5,2,7,4,9,9,6], dtype=int)
#print(len(target))
#alfabeto = np.asarray([0,1,2,3,4,5,6,7,8,9,10], dtype=int)
alfabeto = np.arange(0,11)
shazam(querry, target, alfabeto, 1)
