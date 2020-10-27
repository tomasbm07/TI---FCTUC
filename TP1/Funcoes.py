import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff
from Histograma import histograma

PATH = "data\\"

def group_symbols(info):
    group=2
    new_info=[]
    for i in range(0,int(np.prod(info.shape))-group,group):
        new_info.append(info[i:i+group])
    new_info=np.asarray(new_info)
    return gerar_alfabeto(new_info)

def gerar_alfabeto(file):
	if type(file) is str:	
		# Text
		if ".txt" in file:
		
			file = open(PATH + file, "r")
			info = np.asarray(list(file.read()))

			x = [chr(i) for i in range(ord('a'), ord('z') + 1)]
			x += [chr(i) for i in range(ord('A'), ord('Z') + 1)]
			x = np.asarray(x)
			values = np.zeros(52, dtype=int)

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
	else: # informaçao n vem de nehum ficheiro -> gerar alfabeto de input
		info = np.array(file, copy=True)
        x_groups = []
        for i,j in info:
            if [i,j] not in x_groups:
                x_groups.append([i,j])
        x_groups=np.asarray(sorted(x_groups),dtype=str)
        values=np.zeros(x_groups.shape[0],dtype=int)
        for i,j in info:
            values[np.where(x_groups==np.asarray([i,j],dtype=str))[0]]+=1
        x=np.array([''.join([j for j in i]) for i in x_groups])
	return x, values, info