import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import histograma
from pyitlib import discrete_random_variable as drv
import Funcoes as f

PATH = "data\\"

def plot_it(mutual_information):
	plt.figure(1)
	plt.plot(np.arange(1, len(mutual_information)+1 ), mutual_information, 'o')
	plt.ylabel("Informacao mutua")
	plt.xlabel("Song*x")
	plt.annotate(f'Max: {mutual_information.max():.02f}', xy=(0, 0), xycoords=('axes fraction', 'figure fraction'),
                 xytext=(65, 5), textcoords='offset points', size=12, ha='right', va='bottom')
	plt.show()

def mutual_information(tabela):
	mutual_info=0
	for x in range(len(tabela[:,0])):
		for y in range(len(tabela[:,1])):
			if tabela[x,y]!=0:
				mutual_info += ((tabela[x, y]/tabela.sum()) * (np.log2( (tabela.sum()*tabela[x,y]) / ( (tabela.sum(axis=1)[x])*(tabela.sum(axis=0)[y]) ) )))
	return mutual_info

def shazam(querry, target, alfabeto, step):
	mutual_info = np.zeros( int( np.ceil( (len(target) - len(querry) + 1)/step ) ), dtype=float)
	tabela = np.zeros( ( len( alfabeto ), len( alfabeto ) ), dtype=float)
	index = 0
	for j in range(0,len(target)-len(querry)+1,step):
		#Set the test_target 
		test_target = target[j:j + len(querry)+1] 

		#Set the repetitions values
		for i in range( len(querry) ):
			tabela[ alfabeto==test_target[i], alfabeto==querry[i] ]+=1

		#Probabilidades
		tabela[tabela>0] /= len(querry)

		#Calculate Mutual Information
		mutual_info[index]=mutual_information(tabela)
		index += 1
		tabela = np.zeros((len(alfabeto), len(alfabeto)), dtype=float)
	#print(mutual_info, len(mutual_info))
	return mutual_info

def compare_MIs(songs):
	mt_infos=np.empty(0, dtype=float)
	x, values, info = f.gerar_alfabeto("saxriff.wav")
	for i in songs:
		x2, values2, info2 = f.gerar_alfabeto(i)
		mt_infos=np.append(mt_infos, shazam(info, info2, x, int( 0.25*len(info) ) ).max() )
	plot_it(mt_infos)

querry = np.asarray([2, 6 ,4 ,10 ,5, 9, 5 ,8, 0, 8], dtype=int)
target = np.asarray([6,8,9,7,2,4,9,9,4,9,1,4,8,0,1,2,2,6,3,2,0,7,4,9,5,4,8,5,2,7,8,0,7,4,8,5,7,4,3,2,2,7,3,5,2,7,4,9,9,6], dtype=int)
#print(len(target))
#alfabeto = np.asarray([0,1,2,3,4,5,6,7,8,9,10], dtype=int)
alfabeto = np.arange(0,11)
#shazam(querry, target, alfabeto, 1)


