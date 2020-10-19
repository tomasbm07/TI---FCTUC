import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy
import huffmancodec as huff

PATH = "data\\"


def huffmanCode(data):
	image = np.ndarray(img.imread(PATH + data))


	codec = huff.HuffmanCodec.from_data(image)
	symbols, length = codec.get_code_len()
	print(symbols)
	print(length)