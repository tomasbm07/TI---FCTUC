import HuffmanCode as huff
from Histograma import histograma
import Funcoes as f
import MutualInformation as mt


def main():
	#ficheiros: lena.bmp, CT1.bmp, binaria.bmp, saxriff.wav, texto.txt
	file = "CT1.bmp"
	x, values, info = f.gerar_alfabeto(file)

	"""Exercicios 1, 2 e 3"""
	histograma(x, values)

	"""Exercicio 4"""
	#huff.huffmanCode(info, values)

	"""Exercicio 5"""
	#f.group_symb(info)




if __name__ == "__main__":
	main()
