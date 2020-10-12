import Histograma as hst
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile


PATH = "data\\"


"""img = img.imread(PATH + "lena.bmp")
img = np.asarray(img)
hst.show_histograma(img)"""

img = img.imread(PATH + "CT1.bmp")
img = np.asarray(img)
#print(img[:,:,:3])
hst.show_histograma(img[:,:,:3])

"""img = img.imread(PATH + "binaria.bmp")
img = np.asarray(img)
hst.show_histograma(img)"""

#,sound = wavfile.read(PATH + "saxriff.wav")
#sound = np.asarray(sound)



