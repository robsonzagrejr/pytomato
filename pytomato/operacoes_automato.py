from .Evaristo.functions import read_af_string
from .automato import obj_para_texto

"""Adição de prefixo em estados

Recebe um prefixo o qual será adicionado a todos os estados do automato.
Resolve o problema de estados com mesmo nome em operações envolvendo dois
automatos.
Retorna o mesmo automato porem com os estados posusindo tal prefixo.
"""
def _add_prefixo_estado(prefixo, automato):
    automato_r = {} 
    automato_r['n_estados'] = automato['n_estados']
    automato_r['inicial'] = f"{prefixo}_{automato['inicial']}"
    automato_r['aceitacao'] = [f"{prefixo}_{e}" for e in automato['aceitacao']]
    automato_r['alfabeto'] = automato['alfabeto']
    transicoes = {}
    for estado, trans in automato['transicoes'].items():
        estado_trans = {}
        for simbolo, estados in trans.items():
            estado_trans[simbolo] = [f"{prefixo}_{e}" for e in estados]
        transicoes[f"{prefixo}_{estado}"] = estado_trans
    automato_r['transicoes'] = transicoes    
    return automato_r


"""União de automatos

Recebe dois automatos e faz a união dos mesmos construindo
um automato com um novo estado de aceitação e inicial, fazendo episolon
transições. Renomeia os estados dos automatos que recebeu para previnir
possíveis erros.
"""
def uniao(automato_1, automato_2, prefix_a1 = 'a1', prefix_a2 = 'a2'):
    automato_1_r = _add_prefixo_estado(prefix_a1, automato_1)
    automato_2_r = _add_prefixo_estado(prefix_a2, automato_2)

    automato_u = {}
    automato_u['n_estados'] = int(automato_1_r['n_estados']) + int(automato_1_r['n_estados']) + 2
    automato_u['inicial'] = 'S'
    automato_u['aceitacao'] = ['A']
    automato_u['alfabeto'] = list(
        set(
            automato_1_r['alfabeto']
            + automato_2_r['alfabeto']
            + ['&']
        )
    )

    transicoes = automato_1_r['transicoes'].copy()
    transicoes.update(automato_2_r['transicoes'])
    transicoes[automato_u['inicial']] = {
        '&': [automato_1_r['inicial'], automato_2_r['inicial']]
    }
    antigo_aceitacao = automato_1_r['aceitacao'] + automato_2_r['aceitacao']
    for antigo_a in antigo_aceitacao:
        trans_antigo_a = transicoes.get(antigo_a, {})
        trans_antigo_a['&'] = automato_u['aceitacao']
        transicoes[antigo_a] = trans_antigo_a
    automato_u['transicoes'] = transicoes

    return automato_u 


"""Intercessão de automatos

Recebe dois automatos e faz a intercessão dos mesmos construindo
um automato com o estado de aceitação do automato_2 e inicial do automato_1,
fazendo episolon transições entre o final do automato_1 e o inicio do
automato_2. Renomeia os estados dos automatos que recebeu para previnir
possíveis erros.
"""
def intersecao(automato_1, automato_2):
    automato_1_r = _add_prefixo_estado('a1', automato_1)
    automato_2_r = _add_prefixo_estado('a2', automato_2)

    automato_i = {}
    automato_i['n_estados'] = int(automato_1_r['n_estados']) + int(automato_1_r['n_estados'])
    automato_i['inicial'] = automato_1_r['inicial']
    automato_i['aceitacao'] = automato_2_r['aceitacao']
    automato_i['alfabeto'] = list(
        set(
            automato_1_r['alfabeto']
            + automato_2_r['alfabeto']
            +['&']
        )
    )

    transicoes = automato_1_r['transicoes'].copy()
    transicoes.update(automato_2_r['transicoes'])
    antigo_aceitacao_1 = automato_1_r['aceitacao']
    for antigo_a in antigo_aceitacao_1:
        trans_antigo_a = transicoes.get(antigo_a, {})
        trans_antigo_a['&'] = [automato_2_r['inicial']]
        transicoes[antigo_a] = trans_antigo_a

    automato_i['transicoes'] = transicoes

    return automato_i


def afnd_para_afd_sem_epsilon(afnd):
	afd = {}
	n_estados = 0
	afd['n_estados'] = ""	
	afd['inicial'] = afnd['inicial']	
	afd['aceitacao'] = afnd['aceitacao']
	afd['alfabeto'] = afnd['alfabeto']
	afd['transicoes'] = {}	
	estados_multiplos = {}
	for estado in afnd['transicoes']:
		afd['transicoes'][estado] = {}
		for simbolo in afnd['transicoes'][estado]:
			if len(afnd['transicoes'][estado][simbolo]) > 1:
				str_estados = ""
				for estado_multiplo in afnd['transicoes'][estado][simbolo]:
					str_estados += estado_multiplo
				estados_multiplos[str_estados] = afnd['transicoes'][estado][simbolo]	
				afd['transicoes'][estado][simbolo] = [str_estados]
			else:
				afd['transicoes'][estado][simbolo] = afnd['transicoes'][estado][simbolo]
		n_estados += 1
	while len(estados_multiplos) != 0:
		novo_estados_multiplos = {}
		for estado in estados_multiplos:
			for final in afd['aceitacao']:
				if final in estados_multiplos[estado] and estado not in afd['aceitacao']:
					afd['aceitacao'].append(estado)
			if estado not in afd['transicoes']:
				afd['transicoes'][estado] = {}
				n_estados += 1
			for simbolo in afd['alfabeto']:
				lista_estados = []
				for unidade in estados_multiplos[estado]:
					try:						
						for estado_multiplo in afnd['transicoes'][unidade][simbolo]:
							lista_estados.append(estado_multiplo)
					except:
						continue
				if len(lista_estados) > 1:
					str_estados = ""
					for e in lista_estados:
						str_estados += e
					if str_estados not in afd['transicoes']:
						novo_estados_multiplos[str_estados] = lista_estados
					afd['transicoes'][estado][simbolo] = [str_estados]
				elif len(lista_estados) == 1:
					afd['transicoes'][estado][simbolo] = lista_estados
		
		estados_multiplos = novo_estados_multiplos
	#Contabilizar estados que não tem transicoes de saida
	for estado in afd['transicoes']:
		for simbolo in	afd['transicoes'][estado]:
			if afd['transicoes'][estado][simbolo][0] not in afd['transicoes']:
				n_estados += 1	
	afd['n_estados'] = str(n_estados)
	return afd
	

def afnd_para_afd_com_epsilon(afnd):
	epsilon_fecho = {}
	epsilon_fecho_str = {}
	for estado in afnd['transicoes']:
		fecho = [estado]
		fecho_str = estado
		visitados = [estado]
		while visitados != []:
			proximos_visitados = []
			for visitado in visitados:
				try:
					for e in afnd['transicoes'][visitado]['&']:
						if e not in fecho:
							fecho.append(e)
							fecho_str += e
							proximos_visitados.append(e)
				except:
					continue
			visitados = proximos_visitados
		epsilon_fecho[estado] = fecho
		epsilon_fecho_str[estado] = fecho_str
	afd = {}	
	n_estados = 0
	afd['n_estados'] = ""	
	afd['inicial'] = epsilon_fecho_str[afnd['inicial']]
	afd['aceitacao'] = []
	for estado in afnd['aceitacao']:
		afd['aceitacao'].append(epsilon_fecho_str[estado])
	afd['alfabeto'] = afnd['alfabeto'].copy()
	afd['alfabeto'].remove('&')
	afd['transicoes'] = {}	
	estados_multiplos = {}
	for estado in afnd['transicoes']:
		afd['transicoes'][epsilon_fecho_str[estado]] = {}
		for simbolo in afnd['transicoes'][estado]:
			if simbolo != '&':
				if len(afnd['transicoes'][estado][simbolo]) > 1:
					soma_fecho = []
					for estado_multiplo in afnd['transicoes'][estado][simbolo]:
						for e in epsilon_fecho[estado_multiplo]:
							if e not in soma_fecho:
								soma_fecho.append(e)
					str_estados = ""
					for fecho_multiplo in soma_fecho:
						str_estados += fecho_multiplo
					estados_multiplos[str_estados] = soma_fecho
					afd['transicoes'][epsilon_fecho_str[estado]][simbolo] = [str_estados]
				elif len(epsilon_fecho[afnd['transicoes'][estado][simbolo][0]]) > 1:
					str_estados = ""
					for estado_multiplo in epsilon_fecho[afnd['transicoes'][estado][simbolo][0]]:
						str_estados += estado_multiplo
					estados_multiplos[str_estados] = epsilon_fecho[afnd['transicoes'][estado][simbolo][0]]	
					afd['transicoes'][epsilon_fecho_str[estado]][simbolo] = [str_estados]
				else:
					afd['transicoes'][epsilon_fecho_str[estado]][simbolo] = epsilon_fecho[afnd['transicoes'][estado][simbolo][0]]
		n_estados += 1
	while len(estados_multiplos) != 0:
		novo_estados_multiplos = {}
		for estado in estados_multiplos:
			for final in afnd['aceitacao']:
				if epsilon_fecho_str[final] in estados_multiplos[estado] and estado not in afd['aceitacao']:
					afd['aceitacao'].append(estado)
			if estado not in afd['transicoes']:
				afd['transicoes'][estado] = {}
				n_estados += 1
			for simbolo in afd['alfabeto']:
				lista_estados = []
				for unidade in estados_multiplos[estado]:
					try:						
						for estado_multiplo in afnd['transicoes'][unidade][simbolo]:
							for fecho in epsilon_fecho[estado_multiplo]:
								if fecho not in lista_estados:
									lista_estados.append(fecho)
					except:
						continue
				if len(lista_estados) > 1:
					str_estados = ""
					for e in lista_estados:
						str_estados += e
					if str_estados not in afd['transicoes']:
						novo_estados_multiplos[str_estados] = lista_estados
					afd['transicoes'][estado][simbolo] = [str_estados]
				elif len(lista_estados) == 1:					
						afd['transicoes'][estado][simbolo] = lista_estados
		estados_multiplos = novo_estados_multiplos		
	afd['n_estados'] = str(n_estados)
	return afd
	

def afnd_para_afd(afnd):
	my_texto = obj_para_texto(afnd)
	evaristo_af = read_af_string(my_texto)
	evaristo_af.determinize()
	estrutura = {}
	estrutura['n_estados'] = evaristo_af.n_states
	estrutura['inicial'] = evaristo_af.start_state
	estrutura['aceitacao'] = evaristo_af.accept_states
	estrutura['alfabeto'] = evaristo_af.alphabet
	estrutura['transicoes'] = evaristo_af.transition_table
	return estrutura


def get_inalcancaveis(afd):
	estados_alcancaveis = [afd['inicial'][0]].copy()
	novos_estados = [afd['inicial'][0]].copy()	
	while True:
		temp = []
		for estado in novos_estados:
			try:
				for simbolo in afd['transicoes'][estado]:
					temp.append(afd['transicoes'][estado][simbolo][0])
			except:
				continue
		novos_estados = [estado for estado in temp if estado not in estados_alcancaveis]
		estados_alcancaveis.extend(novos_estados)
		if novos_estados == []:
			break
	estados = []
	for estado in afd['transicoes']:
		if estado not in estados:
			estados.append(estado)
		for simbolo in afd['transicoes'][estado]:
			if afd['transicoes'][estado][simbolo][0] not in estados:
				estados.append(afd['transicoes'][estado][simbolo][0])
			
	estados_inalcancaveis = [estado for estado in estados if estado not in estados_alcancaveis]
	return estados_inalcancaveis


def get_mortos(afd):
	vivos = afd['aceitacao'].copy()
	for vivo in vivos:
		transicoes = afd['transicoes']
		for estado in transicoes.keys():
			for simbolo_do_alfabeto in afd['alfabeto']:
				try:
					if (vivo in transicoes[estado][simbolo_do_alfabeto]) and (not estado in vivos):
						vivos.append(estado)
				except:
					continue
	mortos = []
	for estado in afd['transicoes']:
		if (estado not in vivos) and (estado not in mortos):
			mortos.append(estado)
		for simbolo in afd['transicoes'][estado]:
			if (afd['transicoes'][estado][simbolo][0] not in vivos) and (afd['transicoes'][estado][simbolo][0] not in mortos):
				mortos.append(afd['transicoes'][estado][simbolo][0])
	return mortos
	
def get_classes_equivalencia(afd):
	P = [afd['aceitacao'].copy(),[estado for estado in afd['transicoes'].copy() if estado not in afd['aceitacao']]]
	Q = [afd['aceitacao'].copy()]	
	while Q != []:
		A = Q.pop(0)
		for simbolo in afd['alfabeto']:
			X = []
			for estado in afd['transicoes']:
				try:
					if afd['transicoes'][estado][simbolo][0] in A:
						X.append(estado)
				except:
					continue
			new_P = P
			for Y in P:
				XintersectionY = [estado for estado in X if estado in Y]
				YminusX = [estado for estado in Y if estado not in X]
				if  XintersectionY != [] and YminusX != []:
					new_P.remove(Y)
					new_P.append(XintersectionY)
					new_P.append(YminusX)
					if Y in Q:
						Q.remove(Y)
						Q.append(XintersectionY)
						Q.append(YminusX)
					else:
						if len(XintersectionY) <= len(YminusX):
							Q.append(XintersectionY)
						else:
							Q.append(YminusX)
			P = new_P
			
	classes = {}
	for classe in P:
		nome = ""
		for c in classe:
			nome += c
		classes[nome] = classe
	return classes
	

def minimiza_afd(afd):	
	afd_minimizado = {}	
	afd_minimizado['n_estados'] = ""
	afd_minimizado['inicial'] = ""	
	afd_minimizado['aceitacao'] = []
	afd_minimizado['alfabeto'] = afd['alfabeto']
	afd_minimizado['transicoes'] = {}
		
	#Eliminar os estados inalcançáveis
	estados_inalcancaveis = get_inalcancaveis(afd)
	for estado in estados_inalcancaveis:
		afd['transicoes'].pop(estado, None)
		if estado in afd['aceitacao']:
			afd['aceitacao'].remove(estado)
		afd['n_estados'] = str(int(afd['n_estados'])-1) 
	
	#Eliminar os estados mortos
	estados_mortos = get_mortos(afd)
	for morto in estados_mortos:
		afd['transicoes'].pop(morto, None)
		if estado in afd['aceitacao']:
			afd['aceitacao'].remove(estado)
		afd['n_estados'] = str(int(afd['n_estados'])-1)
		for estado in afd['transicoes']:
			afd['transicoes'][estado] = {key:val for key, val in afd['transicoes'][estado].items() if val != [morto]}		

	afd_minimizado['transicoes'] = {}
	
	#Fundir estados equivalentes			
	classes = get_classes_equivalencia(afd)	
	for classe in classes:
		#q0: CE que contém q0
		if afd['inicial'] in classes[classe]:
			afd_minimizado['inicial'] = classe
			afd_minimizado['transicoes'][classe] = {}
			for simbolo in afd['transicoes'][classes[classe][0]]:
				for classe_destino in classes:
					if afd['transicoes'][classes[classe][0]][simbolo][0] in classe_destino:
						afd_minimizado['transicoes'][classe][simbolo] = [classe_destino]
	for classe in classes:
		if afd['inicial'] not in classes[classe]:
			afd_minimizado['transicoes'][classe] = {}
			for simbolo in afd['transicoes'][classes[classe][0]]:
				for classe_destino in classes:
					if afd['transicoes'][classes[classe][0]][simbolo][0] in classe_destino:
						afd_minimizado['transicoes'][classe][simbolo] = [classe_destino]
		for estado in classes[classe]:
			if estado in afd['aceitacao'] and classe not in afd_minimizado['aceitacao']:
				afd_minimizado['aceitacao'].append(classe)
	
	afd_minimizado['n_estados'] = str(len(classes))

	return afd_minimizado


"""Teste

Main criado para testar as funções.
"""
if __name__ == '__main__':
    print("=============Uniao===========")
    afd_file = open("../examples/AFND_sem_epsilon", "r")
    automato_1 = texto_para_obj(afd_file.read())
    automato_2 = automato_1.copy()
    print(uniao(automato_1, automato_2))

    print("=============Intersecao===========")
    print(intersecao(automato_1, automato_2))

