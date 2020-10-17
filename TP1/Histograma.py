import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import sounddevice as sd
from scipy.io import wavfile
from scipy.stats import entropy

PATH = "data\\"


# Represents a numpy array in a histogram
def show_histograma(data):
    x, values = np.unique(data, return_counts=True)
    plt.figure(0)
    plt.annotate(f'H = {entropy(values):.2f} bits/pixel', xy=(0, 0), xycoords=('axes fraction', 'figure fraction'),
                 xytext=(65, 5), textcoords='offset points', size=12, ha='right', va='bottom')
    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Repetições")
    plt.bar(x, values, align="center")
    plt.show()


# Selects how to represent each file type
def histograma(file):
    # Text
    if ".txt" in file:
        file = open(PATH + file, "r")
        text = np.asarray(list(file.read()))
        show_histograma(text)

    # Images
    if ".bmp" in file:
        image = img.imread(PATH + file)
        # Check se a imagem é RGBA ou Grayscale
        if image.ndim == 2:
            show_histograma(image)  # Grayscale
        else:
            show_histograma(image[:, :, :3])  # RGBA

    # Sound
    if ".wav" in file:
        sr, sound = wavfile.read(PATH + "saxriff.wav")  # returns Sample Rate and Data
        sound = np.asarray(sound)
        show_histograma(sound)
