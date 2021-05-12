import json
from pytomato.gramatica import (
    texto_para_obj
)
from pytomato.conversion_af_gr import (
    search_initial,
    search_non_terminal,
    search_terminal, 
    search_productions
)

def _search_productions(grammar_text):
    _productions = search_productions(grammar_text)
    productions = {}
    for key, val in _productions.items():
        productions[key] = list(val)
    return productions


def define_components(grammar):
    grammar['s_inicial'] = search_initial(grammar['gramatica'])
    grammar['s_n_terminal'] = search_non_terminal(grammar['gramatica'])
    grammar['s_terminal'] = search_terminal(grammar['gramatica'])
    grammar['producoes'] = _search_productions(grammar['gramatica'])

    grammar['first'] = define_first(grammar)
    #grammar['itens'] = search_items(grammar)
    #grammar['follow'] = search_follow(gramatica['gramatica'])
    
    return grammar 


def define_follow(production):
    pass


def find_element_first(element, grammar, firsts={}):
    # Se ja fir o first para o elemento
    if element in firsts.keys():
        print("==================")
        print(f"Element {element} in firsts")
        return firsts[element], firsts

    elif element in grammar['s_terminal']: # Epsilon é considerado um terminal
        print("==================")
        print(f"Element {element} is terminal")
        return [element], firsts

    elif element in grammar['s_n_terminal']:
        print("==================")
        print(f"Element {element} is nao terminal")
        first = []
        for production in grammar['producoes'][element]:
            # 2.a Se aY entao 'a' esta em FIRST
            if production[0] not in grammar['s_n_terminal']:
                print(f"produção {production} start with terminal")
                first.append(production[0])

            # 2.b Se Epsilon faz parte da produção, entao ele entra no FIRST
            elif "&" == production:
                print(f"produção {production} is Epsilon")
                first.append("&")

            # 2.c Se Y1Y2... entao FIRST recebe FIRST(Y1)
            else:
                print(f"produção {production} começa com n terminal")
                for s in production:
                    print(f"iniciando com {s}")
                    s_first, s_firsts = find_element_first(s, grammar, firsts)
                    print(f"First de {s} -> {s_first}")
                    # Caso ainda n tenha feita o first para 's'
                    if s not in firsts.keys():
                        s_firsts[s] = s_first
                        firsts.update(s_firsts)

                    first += s_first
        return list(set(first)), firsts
    return [], {}



def define_first(grammar):
    symbols = grammar['s_terminal'] + grammar['s_n_terminal']
    firsts = {}
    for s in symbols:
        s_first, s_firsts = find_element_first(s, grammar, firsts)
        firsts.update(s_firsts)
        if s not in firsts:
            firsts[s] = s_first

    return firsts


def define_closure(item, grammar):
    while True:
        add_new_item = False
        for i in item:
            production = i[0][1]
            aux_B = production.split('.')[1]
            if aux_B:
                B = aux_B[0]
                a = i[1]
                if B in grammar['s_n_terminal']:
                    for gama in grammar['producoes'][B]:
                        for b in find_element_first(f"{B}{a}", grammar):
                            add_new_item = True
                            item.append((B, f".{gama}"), b)
        if not add_new_item:
            break

    return item


def define_goto(item, symbol, grammar):
    j = set()
    breakpoint()

    return []


def search_items(grammar):
    #((cabeça, corpo), terminal/$)
    closer_i0 = define_closure([(("S'", ".S"), "$")])
    items = {
        'I0': {"$" : closer_i0}
    }
    symbols = list(set(grammar['s_n_terminal'] + grammar['s_terminal']))
    aux = 1

    while True:
        add_new_item = False
        for item in items.values():
            for symbol in symbols:
                goto_item_symbol = define_goto(item, symbol, grammar)
                if goto_item_symbol and (goto_item_symbol not in items.values()):
                    items[f'I{aux}'] = goto_item_symbol
                    add_new_item = True
                    aux += 1

        if not add_new_item:
            break

    return items
    

if "__name__" == "__main__":
    "d > c"
    grammar_text = f"""
S'->S
S->CC
C->cC | d
    """
    grammar_dict = texto_para_obj(grammar_text, 'GLC_Test')
    glc = define_components(grammar_dict)
    print(json.dumps(glc, ident=4))
