import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import histograma
import Funcoes as f



def shazam(querry, target, alfabeto, step):
	mutual_info = np.zeros( int(np.ceil((len(target) - len(querry) + 1)/step) ), dtype=float)
	tabela = np.zeros( ( len(alfabeto), len(alfabeto) ), dtype=float)
	index = 0

	for j in range(0,len(target)-len(querry)+1,step):
		#Set the test_target 
		test_target = target[j:j + len(querry)] 

		#Set the repetitions values
		for i in range(len(querry)):
			tabela[ alfabeto==test_target[i], alfabeto==querry[i] ]+=1

		#Probabilidades
		tabela[tabela>0] /= len(querry)

		#Calculate Mutual Information
		mutual_info[index]=calc_mt_info(tabela)
		index += 1
		tabela = np.zeros((len(alfabeto), len(alfabeto)), dtype=float)

	print(mutual_info, len(mutual_info))
	return mutual_info


def calc_mt_info(tabela):
	mutual_info=0
	for x in range(len(tabela[0,:])):
		for y in range(len(tabela[:,0])):
			if tabela[x,y]!=0:
				mutual_info += ((tabela[x, y]/tabela.sum()) * (np.log2( (tabela.sum()*tabela[x,y]) / ( (tabela.sum(axis=1)[x])*(tabela.sum(axis=0)[y]) ) )))
	return mutual_info


def graph_IM(target):
	im = []
	x, values, info = f.gerar_alfabeto("saxriff.wav") #querry
	x2, values2, info2 = f.gerar_alfabeto(target) #target
	im = shazam(info, info2, x, int((len(info)/4)))

	sr, data = wavfile.read("data\\"+target)
	plt.plot(np.arange(0, int(len(info2)/sr), (len(info2)/len(im))/sr), im)
	plt.title(f"Evolução Informação mútua em {target}")
	plt.xlabel("Tempo(s)")
	plt.ylabel("Informação Mútua")
	plt.grid()
	plt.show()


"""
#Simulação
idk = []
#querry = np.asarray([2,6,4,10,5,9,5,8,0,8], dtype=int)
querry = np.asarray([1,2,3,4,5,6,7,8,9,10], dtype=int)
target = np.asarray([6,8,9,7,2,4,9,9,4,9 ,1,4,8,0,1,2,1,2,3,4,5,6,7,8,9,10,8,5,2,7,8,0,7,4,8,5,7,4,3,2,2,7,3,5,2,7,4,9,9,6], dtype=int)
alfabeto = np.asarray([0,1,2,3,4,5,6,7,8,9,10], dtype=int)
idk = shazam(querry, target, alfabeto, 1)
plt.plot(np.arange(0, 41, 1), idk)

plt.title("Simulação")
plt.ylabel("Informação Mútua")
plt.xlabel("nº janela")
plt.grid()
plt.show()"""
