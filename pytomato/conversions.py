from collections import defaultdict
class RegularGrammar():
	def __init__(self, gramatica_inicial,gramatica_nao_terminais,gramatica_terminais,regras_producao):
		self.gramatica_inicial = gramatica_inicial
		self.gramatica_nao_terminais = gramatica_nao_terminais
		self.gramatica_terminais = gramatica_terminais
		self.regras_producao = regras_producao
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
	regras_producao = dict(regras_producao)	
	gram = RegularGrammar(gramatica_inicial,gramatica_nao_terminais,gramatica_terminais,regras_producao)
	return gram
def gramatica_para_afd(gram):
	afd = {}
	afd['n_estados'] = len(gram.gramatica_nao_terminais)
	afd['inicial'] = gram.gramatica_inicial	
	afd['aceitacao'] = ['new_final_state']
	afd['alfabeto'] = gram.gramatica_terminais
	afd['transicoes'] = {}
	if ('&' in gram.regras_producao['{}'.format(gram.gramatica_inicial)]):
		afd['aceitacao'].append(afd['inicial'])	
	for a in gram.gramatica_nao_terminais:
		afd['transicoes'][a] = {}
	for a,b in gram.regras_producao.items():
		aux = list(b)
		for x in aux:
			if len(x) == 2:
				afd['transicoes'][a][x[0]] = x[1]
	for a,b in gram.regras_producao.items():
		aux = list(b)
		for x in aux:
			if len(x) == 1:
				afd['transicoes'][a] = 'new_final_state'	
	return afd