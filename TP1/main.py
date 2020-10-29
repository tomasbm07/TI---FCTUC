import HuffmanCode as huff
from Histograma import histograma
import Funcoes as f

PATH = "data\\"


def main():
	#lena.bmp, CT1.bmp, binaria.bmp, saxriff.wav, texto.txt
	x, values, info = f.gerar_alfabeto("CT1.bmp")

	"""Exercicios 1, 2 e 3"""
	#histograma(x, values)

	"""Exercicio 4"""
	#huff.huffmanCode(info, values)

	"""Exercicio 5"""
	f.group_items(info)

	# Exercicio 6
	

if __name__ == "__main__": 
    main()
