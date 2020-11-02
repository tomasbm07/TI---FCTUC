import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import histograma
import math


PATH = "data\\"


def shazam(querry, target, alfabeto, step):
	alfabeto = np.asarray(alfabeto,  dtype=int)
	mutual_info = np.zeros(len(target) - len(querry) + 1, dtype=float)
	tabela = np.zeros((len(alfabeto), len(alfabeto)), dtype=float)
	index = 0


	for j in range(len(target)-1):
		#Set the test_target 
		test_target = np.asarray(target[j*step:j*step + len(querry)])
		if len(test_target)<len(querry):
			break
		#Set the repetitions values
		for i in range(len(querry)):
			tabela[test_target[i]==alfabeto, querry[i]==alfabeto]+=1

			if i == len(querry)-1:
				#Probabilidade
				tabela[tabela>0] /= len(querry)
				#Calculate Mutual Information
				for x in range(len(querry)-1):
					for y in range(len(test_target)-1):
						if tabela[x,y] != 0:
							mutual_info[index] += (tabela[x,y]/tabela.sum()) * (np.log2( (tabela.sum()*tabela[x,y]) / ( (tabela.sum(axis=1)[x])*(tabela.sum(axis=0)[y]) ) ))
							#mutual_info[index] += tabela[x,y] * (math.log2(tabela[x,y]) - (math.log2(tabela.sum(axis=0)[y])) - (math.log2(tabela.sum(axis=1)[x])))
				
				print(tabela)
				print("info: ", mutual_info[index])
				print("sum: ", tabela.sum())
				print("\n\n")

				index += 1
				tabela = np.zeros((len(alfabeto), len(alfabeto)), dtype=float)

	print(mutual_info, len(mutual_info))



querry = np.asarray([2,6,4,10,5,9,5,8,0,8], dtype=int)
target = np.asarray([6,8,9,7,2,4,9,9,4,9 ,1,4,8,0,1,2,2,6,3,2,0,7,4,9,5,4,8,5,2,7,8,0,7,4,8,5,7,4,3,2,2,7,3,5,2,7,4,9,9,6], dtype=int)
alfabeto = np.asarray([0,1,2,3,4,5,6,7,8,9,10], dtype=int)

#shazam(querry, target, alfabeto, 1)
