import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff

PATH = "data\\"


def huffmanCode(file):
	# Images
	if ".bmp" in file:
		image = np.asarray(img.imread(PATH + file))
		codec = huff.HuffmanCodec.from_data(image[:, :, :1].tobytes())
		symbols, length = codec.get_code_len()
		print(f"{entropy(length, base=2):.2f}")
