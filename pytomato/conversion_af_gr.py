from collections import defaultdict
import copy
# usado para construir classe RegularGrammar a partir do construtor
def search_initial(gramatica):
	if 'S\'' in gramatica:
		return 'S\''
	else:
		return 'S'


# usado para construir classe RegularGrammar a partir do construtor		
def search_non_terminal(gramatica):
	return list(gramatica.keys())
# usado para construir classe RegularGrammar a partir do construtor
def search_terminal(gramatica):
    terminais=[]
    for nonterm,list_prod in gramatica.items():
        for i in list_prod:
            if i.islower():
                i = i.replace('\r', '')
                i = i.replace('\n', '')
                terminais.append(i)
    return terminais


# usado para construir classe RegularGrammar a partir do construtor
def search_productions(gramatica):
	prod_dict=defaultdict(set)
	for nonterm,list_prod in gramatica.items():
		for i in list_prod:
			prod_dict[nonterm].add(i)
	prod_dict = dict(prod_dict)
	return prod_dict


# instancia uma classe de gramatica regular a partir do dicionario
def create_grammar_with_dict(arg_dict):
    nome = arg_dict['nome']
    gramatica_inicial = search_initial(arg_dict['gramatica'])
    gramatica_nao_terminais = search_non_terminal(arg_dict['gramatica'])
    gramatica_terminais = search_terminal(arg_dict['gramatica'])
    regras_producao = search_productions(arg_dict['gramatica'])
    return RegularGrammar(nome, gramatica_inicial,gramatica_nao_terminais,gramatica_terminais,regras_producao)


class RegularGrammar():
    # Encontra se existe alguma & produção (que não esteja no símbolo inicial da gram)
    def epsilon_free(self):
        for head, body in self.regras_producao.items():
            if head != self.gramatica_inicial:
                for production in body:
                    if production == '&':
                        return False
        return True
    # instancia uma glc, remove recursões, se receber uma gramatica sem & producoes.
    def remove_left_recursions(self):        
        GLC = copy.deepcopy(self)
        # se GLC nao for livre de & prod
        if not GLC.epsilon_free():
            return "Gramatica possui & prod, algoritmo nao funciona para gramáticas com & producoes"
        heads_list = list(GLC.gramatica_nao_terminais)
        for i in range(len(heads_list)):
            # resolvendo recursoes indiretas
            # para todos os simbolos em heads_list[i]
            for j in range(i):
                store = []
                productions = []
                if heads_list[i] in GLC.regras_producao:
                    for p in GLC.regras_producao[heads_list[i]]:
                        # se heads_list[j]store pertence a uma das producoes de heads_list[i]
                        if len(p) > 1 and p[0] == heads_list[j]:
                            # producao a armazenar
                            store.append(p[1:])
                            # producao a remover
                            productions.append(p)
                    for k in range(len(productions)):
                        # remover a producao de heads_list[i]
                        GLC.regras_producao[heads_list[i]].remove(productions[k])
                        heads_list_j_body = GLC.regras_producao.get(heads_list[j])
                        # se heads_list[j] existir como cabeca
                        if heads_list_j_body:
                            # adicionar as prod de heads_list[j] (concatenado com valores armazenados em store)
                            # no corpo de heads_list[i]
                            for p in heads_list_j_body:
                                GLC.regras_producao[heads_list[i]].add(p + store[k])
            # recursoes diretas
            new_head = heads_list[i] + "'"
            new_body = set()
            to_keep = set()
            # caso o terminal seja cabeca de alguma prod
            if heads_list[i] in GLC.regras_producao:
                for p in GLC.regras_producao[heads_list[i]]:
                    # Se houver recursao direta a esquerda da produção
                    if p[0] == heads_list[i]:
                        # concatenar o restante da producao mais a nova cabeça no novo corpo
                        new_body.add(p[1:] + new_head)
                    else:
                        to_keep.add(p + new_head)
                # se alguma recursao direta foi encontrada atualizar as cabecas
                if new_body:
                    GLC.regras_producao[heads_list[i]] = to_keep
                    new_body.add('&')
                    GLC.regras_producao[new_head] = new_body
        novos_nao_terminais = set()
        for nao_terminal in GLC.regras_producao.keys():
            novos_nao_terminais.add(nao_terminal)
        GLC.gramatica_nao_terminais = novos_nao_terminais
        return GLC
    # retorna a gramática em forma de dicionario
    def asdict(self):
        regras={}
        for a,b in self.regras_producao.items():
            regras[a] = list(b)
        dic={'nome': self.nome, 'gramatica': regras}
        return dic
    def __init__(self, nome, gramatica_inicial,gramatica_nao_terminais,gramatica_terminais,regras_producao):
        self.nome = nome
        self.gramatica_inicial = gramatica_inicial
        self.gramatica_nao_terminais = gramatica_nao_terminais
        self.gramatica_terminais = gramatica_terminais
        self.regras_producao = regras_producao
    def __str__(self):
        return "inicial:{}\nnao_term:{}\nterm:{}\nregr_prod:{}".format(self.gramatica_inicial,self.gramatica_nao_terminais,self.gramatica_terminais,self.regras_producao)


def get_afd_states(afd):
    states = set()
    for i in afd['transicoes']:
        states.add(i)        
    for i in afd['aceitacao']:
        states.add(i)
    states.add(afd['inicial'])
    return list(states)


def afd_para_gramatica(nome, estrutura):
    gramatica_inicial = estrutura['inicial']
    gramatica_nao_terminais = get_afd_states(estrutura)    
    gramatica_terminais = list(set(estrutura['alfabeto']))
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
    gram = RegularGrammar(nome, gramatica_inicial,gramatica_nao_terminais,gramatica_terminais,regras_producao)        
    gram = gram.asdict()
    return gram

'''
construct an -free regular grammar G' from G (see relevant section);
create a FSA M, with a state for every non-terminal in G'. Set the state representing the start symbol to be the start state;
add another state D, which is terminal;
if the production S is in G' (where S is the start symbol of G', set the state representing S to be final;
for every production AaB in G, add a transition from state A to state B labelled with terminal a;
for every production Aa in G, add a transition from A to the terminal state D
'''
def gramatica_para_afd(gram_dict):
    gram = create_grammar_with_dict(gram_dict)
    afd = {}
    afd['n_estados'] = len(gram.gramatica_nao_terminais) + 1
    afd['inicial'] = gram.gramatica_inicial	
    afd['aceitacao'] = ['T']
    afd['alfabeto'] = gram.gramatica_terminais
    afd['transicoes'] = defaultdict(dict)	
    if ('&' in gram.regras_producao['{}'.format(gram.gramatica_inicial)]):
        afd['aceitacao'].append(afd['inicial'])	
    for non_term in gram.gramatica_nao_terminais:		
        afd['transicoes'][non_term] = defaultdict(list)	
    for head,body in gram.regras_producao.items():
        aux = list(body)
        for x in aux:
            x = x.replace('\r', '')
            x = x.replace('\n', '')
            if len(x) == 2:				
                #for every rule of the form A->aB, we add a transition from state A to state B labelled a				
                afd['transicoes'][head][x[0]].append(x[1])
            if len(x) == 1:				
                # for every rule of the form A->a, we add a transition from state A to state t_state labelled a
                afd['transicoes'][head][x[0]].append('T')	
    afd['transicoes'] = dict(afd['transicoes'])
    for non_term in gram.gramatica_nao_terminais:
        afd['transicoes'][non_term] = dict(afd['transicoes'][non_term])
    # na verdade afd eh um afnd, deve-se determiniza-lo
    return afd

