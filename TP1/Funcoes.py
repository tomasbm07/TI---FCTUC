import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import histograma

PATH = "data\\"

#gera o alfabeto para cada tipo de imagem
def gerar_alfabeto(file):
	# Text
	if ".txt" in file:
		fich = open(PATH + file, "r")
		info = np.asarray(list(fich.read()))

		x = [chr(i) for i in range(ord('a'), ord('z') + 1)]
		x += [chr(i) for i in range(ord('A'), ord('Z') + 1)]
		x = np.asarray(x)
		values = np.zeros(52, dtype=int)

		new_info=info
		for i in new_info:
			if ~np.any(x==i):
				info=np.delete(info, info==i)
		for i in info:
			values[x==i] += 1

	# Images
	if ".bmp" in file:
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
	if ".wav" in file:
		sr, sound = wavfile.read(PATH + file)  # returns Sample Rate and data
		info = np.asarray(sound)
		x = np.asarray([i for i in range(0, 255 + 1)])
		values = np.zeros(255 + 1, dtype=int)
		info=info[:,:1].flatten()
		for i in info:
			values[x==i] += 1
	
	return x, values, info


def group_symbols(info):
	group = 2
	new_info = []
	for i in range(0, int(np.prod(info.shape)) - group, group):
		new_info.append(info[i:i + group])
	new_info = np.asarray(new_info)
	return idk(new_info)


def idk(info):
	info = np.array(info)
	dtype = int if 'int' in str(type(info[0,0])) else str
	x_groups = np.empty([0,2],dtype=dtype)
	print(len(info.tolist()))
	print(info)

	for i, j in info:
		isin=np.array( [ ( x_groups == np.array([i,j], dtype=dtype) )[k,:].all() for k in range( len( x_groups.tolist() ) ) ] , dtype=bool)
		if not isin.any() or len(isin.tolist()) == 0:
			x_groups = np.append(x_groups, np.array([[i, j]], dtype=dtype),axis=0)

	print(x_groups)
	#x_groups=np.sort(x_groups,axis=1)
	values=np.zeros(x_groups.shape[0],dtype=int)
	for i,j in info:
		true_rows= np.array( [(x_groups == np.array([i,j], dtype=dtype) )[k,:].all() for k in range( len( x_groups.tolist() ) ) ] , dtype=bool)
		values[ true_rows ]+=1

	x_groups=np.array([''.join([str(j) for j in i]) for i in x_groups],dtype=str)

	#print(x_groups)

	histograma(x_groups, values)

	return x_groups, values, info