from Histograma import histograma
import HuffmanCode as huff


def main():
	# Exercicios 1, 2 e 3
	# lena.bmp, CT1.bmp, binaria.bmp, saxriff.wav, texto.txt
	inputa = "CT1.bmp"
	histograma(inputa)

	# Exercicios 4 e 5
	huff.huffmanCode(inputa)
	
	





if __name__ == "__main__":
    main()
