import huffmancodec as huff
from Histograma import histograma
import Funcoes as f

PATH = "data\\"


def main():
	# Exercicios 1, 2 e 3
	# lena.bmp, CT1.bmp, binaria.bmp, saxriff.wav, texto.txt
	x, values, idk = f.gerar_alfabeto("CT1.bmp")
	histograma(x, values)

	#huff.huffmanCode("lena.bmp")
	 

if __name__ == "__main__":
    main()
