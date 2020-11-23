import numpy as np

def gerar_alfabeto(file):
    # Text
    if ".txt" in file:
        fich = open(file, "r")
        info = np.asarray(list(fich.read()))

        x = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        x += [chr(i) for i in range(ord('a'), ord('z') + 1)]
        x+=['.',' ',',']

        x = np.asarray(x)
        values = np.zeros(len(x), dtype=int)

        # retirar os carateres a mais do array lido do texto
        new_info = info
        for i in new_info:
            if ~np.any(x == i):
                info = np.delete(info, info == i)

        # Set values(Repetiçoes)
        for i in info:
            values[x == i] += 1
    return x,values,info