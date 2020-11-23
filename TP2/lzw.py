import numpy as np

def LZW(info):
	"""ver carateres unicos da info"""
	index = 0; dic={}
	for i in range(ord('a'), ord('z')+1):
		dic.update( { chr(i):index } )
		index+=1
	""" executar ciclo """

	i = 1
	aux=''
	cod=np.empty(0, dtype=int)
	while i<len(info):
		if aux + info[i] in dic:
			aux += info[i]
		else:
			dic[aux + info[i]] = index
			cod=np.append(cod, dic[aux])
			aux=info[i]
		index+=1
		i+=1
	return (cod)

def other(info):
	"""ver carateres unicos da info"""
	index = 0;
	dic = {}
	for i in range(ord('a'), ord('z') + 1):
		dic.update({chr(i): index})
		index += 1
	""""""

	ret = []
	buffer = ''
	for i in range(0, len(info)):
		c = info[i]

		if len(buffer) == 0 or (buffer + c) in dic:
			buffer = buffer + c
		else:
			code = dic[buffer]
			dic[buffer + c]=index
			buffer = c
			ret = ret + [code]
	if buffer:
		ret = ret + [dic[buffer]]
	return ret
def decodLZW(info):
	"""ver carateres unicos da info"""
	index = 0;	dic = {}
	for i in range(ord('a'), ord('z') + 1):
		dic.update({chr(i): index})
		index += 1
	""""""
	last_symbol = info[0]
	ret = dic[last_symbol]
	for symbol in info[1:]:
		if symbol in dic:
			current = dic[symbol]
			previous = dic[last_symbol]
			to_add = current[0]
			dic[previous + to_add]=index
			ret = ret + current
		else:
			previous = dic[last_symbol]
			to_add = previous[0]
			dic[previous + to_add]=index
			ret = ret + previous + to_add
		index+=1
		last_symbol = symbol
	return ret

