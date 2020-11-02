import HuffmanCode as huff
from Histograma import histograma
import Funcoes as f
import MutualInformation as mt 

PATH = "data\\"


def main():
	#lena.bmp, CT1.bmp, binaria.bmp, saxriff.wav, texto.txt
	x, values, info = f.gerar_alfabeto("saxriff.wav")

	"""Exercicios 1, 2 e 3"""
	#histograma(x, values)

	"""Exercicio 4"""
	#huff.huffmanCode(info, values)

	"""Exercicio 5"""
	#f.group_symb(info)

	"""Exercicio 6"""
	x2, values2, info2 = f.gerar_alfabeto("target01 - repeat.wav")
	mt.shazam(info, info2, x, int(0.25*(len(info2))))


if __name__ == "__main__":
	main()

