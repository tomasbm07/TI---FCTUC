# !/usr/bin/python
# coding: utf-8

import sys
import random
import numpy as np

class lz77:
    def __init__(self, window_size = 65535, buffer_size=255):
        """
           Carrega os parâmetros de tamanho de janela e buffer
           de look-ahead
        """
        self.window_size = window_size
        self.buffer_size = buffer_size
    def encode(self, str):
        ret = []
        i = 0
        while i < len(str):
            begin_window = i-self.window_size
            if begin_window < 0:
                begin_window = 0
            window = str[begin_window:i]
            buffer = str[i:i+self.buffer_size]
            tuple = (0, 0, str[i])

            for size in range(len(buffer), 0, -1):
                index = window.rfind(buffer[0:size])
                if index >= 0:
                    literal = '' # a string vazia representa
                                 # o final do arquivo.
                    if i + size < len(str):
                        literal = str[i+size]
                    tuple = (len(window)-index-1, size, literal)
                    break
            i = i + tuple[1] + 1
            ret = ret + [tuple]
        return ret
    def decode(self, list):
        """
            A decodificação é extremamente simples: basta copiar a
            subsequência indicada pela tupla para o final da sequência
            de saída e acrescentar o novo carácter literal.
        """
        ret = ''
        for tuple in list:
            pos = len(ret) - tuple[0] - 1
            ret = ret + ret[pos:pos+tuple[1]] + tuple[2]
        return ret

def entropia(valores):
    total = np.sum(valores)
    prob = valores[valores > 0] / total
    return np.sum(-np.log2(prob) * (prob))

if __name__=='__main__':
    arr = np.array([random.randint(0, 255) for i in range(50000)])
    encoder = lz77()
    encoded = encoder.encode(arr)
    print(len(encoded), len(arr))
    x1,v1 = np.unique(arr, return_counts=True)
    x2, v2 = np.unique(encoded, return_counts=True)
    print(entropia(v1), entropia(v2))