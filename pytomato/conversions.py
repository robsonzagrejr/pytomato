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

