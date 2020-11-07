import HuffmanCode as huff
from Histograma import histograma
import Funcoes as f
import MutualInformation as mt 

PATH = "data\\"


def main():
	#lena.bmp, CT1.bmp, binaria.bmp, saxriff.wav, texto.txt
	x, values, info = f.gerar_alfabeto("texto.txt")
	"""Exercicios 1, 2 e 3"""
	#histograma(x, values)

	"""Exercicio 4"""
	#huff.huffmanCode(info, values)


	"""Exercicio 5"""
	x, values , info = f.group_symb(info)

	"""Exercicio 6"""
	#songs = ("Song01.wav", "Song02.wav", "Song03.wav", "Song04.wav", "Song05.wav", "Song06.wav", "Song07.wav")
	#mt.compare_MIs(songs)

if __name__ == "__main__": 
    main()

