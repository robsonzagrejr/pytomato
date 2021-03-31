from collections import defaultdict
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
				symbol = x + i
			regras_producao[state].add(symbol)			
			if after_transition_state in estrutura['aceitacao']:
				regras_producao[state].add(x)	
	if estrutura['inicial'] in estrutura['aceitacao']:	
		regras_producao["S'"] = regras_producao[gramatica_inicial].union('&')
		gramatica_inicial = "S'"	
	print(gramatica_inicial)
	print(gramatica_nao_terminais)
	print(gramatica_terminais)
	regras_producao = dict(regras_producao)
	print(regras_producao)	
	return (regras_producao, gramatica_inicial, gramatica_nao_terminais, gramatica_terminais)
def gramatica_para_afnd(estrutura):
	pass