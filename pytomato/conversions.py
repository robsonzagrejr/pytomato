from collections import defaultdict
class RegularGrammar():
	def __init__(self, gramatica_inicial,gramatica_nao_terminais,gramatica_terminais,regras_producao):
		self.gramatica_inicial = gramatica_inicial
		self.gramatica_nao_terminais = gramatica_nao_terminais
		self.gramatica_terminais = gramatica_terminais
		self.regras_producao = regras_producao
	def __str__(self):
		return "inicial:{}\nnao_term:{}\nterm:{}\nregr_prod:{}".format(self.gramatica_inicial,self.gramatica_nao_terminais,self.gramatica_terminais,self.regras_producao)
def get_afd_states(afd):
	states = []
	for i in afd['transicoes']:
		states.append(i)
	return states
def afd_para_gramatica(estrutura):
	gramatica_inicial = estrutura['inicial']
	gramatica_nao_terminais = get_afd_states(estrutura)
	gramatica_terminais = estrutura['alfabeto']	
	#dict subclass that calls a factory function to supply missing values,setting defaultdict to set makes the defaultdict useful for building a dictionary of sets
	regras_producao = defaultdict(set)
	for state, transition in estrutura['transicoes'].items():		
		for x, after_transition_state in transition.items():			
			for i in after_transition_state:
				# constrou producao tipo aB
				symbol = x + i
				regras_producao[state].add(symbol)
			if after_transition_state[0] in estrutura['aceitacao']:				
				# constroi producao do tipo a
				regras_producao[state].add(x)
	# significa que palavra vazia pertence a linguagem, entao precisa derivar epsilon a partir do estado init da gram
	if estrutura['inicial'] in estrutura['aceitacao']:	
		regras_producao["S'"] = regras_producao[gramatica_inicial].union('&')
		gramatica_inicial = "S'"	
	regras_producao = dict(regras_producao)	
	gram = RegularGrammar(gramatica_inicial,gramatica_nao_terminais,gramatica_terminais,regras_producao)
	return gram
'''
construct an -free regular grammar G' from G (see relevant section);
create a FSA M, with a state for every non-terminal in G'. Set the state representing the start symbol to be the start state;
add another state D, which is terminal;
if the production S is in G' (where S is the start symbol of G', set the state representing S to be final;
for every production AaB in G, add a transition from state A to state B labelled with terminal a;
for every production Aa in G, add a transition from A to the terminal state D
'''
def gramatica_para_afd(gram):
	afd = {}
	afd['n_estados'] = len(gram.gramatica_nao_terminais) + 1
	afd['inicial'] = gram.gramatica_inicial	
	afd['aceitacao'] = ['t_state']
	afd['alfabeto'] = gram.gramatica_terminais
	afd['transicoes'] = defaultdict(dict)	
	if ('&' in gram.regras_producao['{}'.format(gram.gramatica_inicial)]):
		afd['aceitacao'].append(afd['inicial'])	
	for non_term in gram.gramatica_nao_terminais:		
		afd['transicoes'][non_term] = defaultdict(list)	
	for head,body in gram.regras_producao.items():
		aux = list(body)
		for x in aux:
			if len(x) == 2:				
				#for every rule of the form A->aB, we add a transition from state A to state B labelled a				
				afd['transicoes'][head][x[0]].append(x[1])
			if len(x) == 1:				
				# for every rule of the form A->a, we add a transition from state A to state t_state labelled a
				afd['transicoes'][head][x[0]].append('t_state')	
	afd['transicoes'] = dict(afd['transicoes'])
	for non_term in gram.gramatica_nao_terminais:
		afd['transicoes'][non_term] = dict(afd['transicoes'][non_term])
	# na verdade afd eh um afnd, deve-se determiniza-lo
	return afd

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
					for e in afnd['transicoes'][visitado]['ε']:
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
	afd['alfabeto'].remove('ε')
	afd['transicoes'] = {}	
	estados_multiplos = {}
	for estado in afnd['transicoes']:
		afd['transicoes'][epsilon_fecho_str[estado]] = {}
		for simbolo in afnd['transicoes'][estado]:
			if simbolo != 'ε':
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
	if 'ε' in afnd['alfabeto']:
		return afnd_para_afd_com_epsilon(afnd)
	else:
		return afnd_para_afd_sem_epsilon(afnd)

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
	estados_inalcancaveis = [estado for estado in afd['transicoes'] if estado not in estados_alcancaveis]
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
		afd['n_estados'] = str(int(afd['n_estados'])-1) 
		
	#Eliminar os estados mortos
	estados_mortos = get_mortos(afd)
	for morto in estados_mortos:
		afd['transicoes'].pop(morto, None)
		afd['n_estados'] = str(int(afd['n_estados'])-1)
		for estado in afd['transicoes']:
			afd['transicoes'][estado] = {key:val for key, val in afd['transicoes'][estado].items() if val != [morto]}		
	
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
