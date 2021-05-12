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
    grammar['itens'] = search_items(grammar)
    #grammar['follow'] = search_follow(gramatica['gramatica'])
    
    return grammar 


def define_follow(production):
    pass


def find_element_first(element, grammar, firsts={}):
    # Se ja fir o first para o elemento
    if element in firsts.keys():
        return firsts[element], firsts

    elif element in grammar['s_terminal']: # Epsilon é considerado um terminal
        return [element], firsts

    elif element in grammar['s_n_terminal']:
        first = []
        for production in grammar['producoes'][element]:
            # 2.a Se aY entao 'a' esta em FIRST
            if production[0] not in grammar['s_n_terminal']:
                first.append(production[0])

            # 2.b Se Epsilon faz parte da produção, entao ele entra no FIRST
            elif "&" == production:
                first.append("&")

            # 2.c Se Y1Y2... entao FIRST recebe FIRST(Y1)
            else:
                for s in production:
                    s_first, s_firsts = find_element_first(s, grammar, firsts)
                    # Caso ainda n tenha feita o first para 's'
                    if s not in firsts.keys():
                        s_firsts[s] = s_first
                        firsts.update(s_firsts)
                    first += s_first

                    #Para a busca caso Epsilon n esteja no first de 's'
                    if "&" not in s_first:
                        break
        return list(set(first)), firsts
    return [], {}



def define_first(grammar):
    symbols = grammar['s_n_terminal'] + grammar['s_terminal']
    firsts = {}
    for s in symbols:
        s_first, s_firsts = find_element_first(s, grammar, firsts)
        firsts.update(s_firsts)
        if s not in firsts:
            firsts[s] = s_first

    return firsts


def find_first_in_expression(expression, grammar):
    symbols = grammar['s_n_terminal'] + grammar['s_terminal']
    first = []
    for e in expression:
        e_first = []
        if e in symbols:
            e_first = grammar['first'][e]
        elif e != '&':
            e_first.append(e)
        first += e_first
        if "&" not in e_first:
            break

    return first
    


def define_closure(item, grammar):
    while True:
        add_new_item = False
        for i in item:
            production = i[0][1]
            aux_B = production.split('.')[1]
            if aux_B:
                B = aux_B[0]
                beta = aux_B[1:] if len(aux_B) > 1 else ''
                a = i[1]
                if B in grammar['s_n_terminal']:
                    for gama in grammar['producoes'][B]:
                        beta_first, beta_firsts = find_element_first(beta, grammar)
                        b_firsts = beta_first
                        if ('&' in beta_first) or not b_firsts:
                            b_firsts += a.split('|')

                        b_firsts = sorted(b_firsts)
                        if b_firsts == ['c']:
                            breakpoint()
                        n_item = ((B, f".{gama}"), "|".join(b_firsts))
                        if n_item not in item:
                            add_new_item = True
                            item.append(n_item)
        if not add_new_item:
            break

    return item


def define_goto(item, symbol, grammar):
    j = []
    for i in item:
        production = i[0][1]
        alpha, symbol_beta = production.split('.')
        if len(symbol_beta) > 0:
            if symbol_beta[0] == symbol:
                beta = symbol_beta[1:] if len(symbol_beta) > 1 else ''
                new_i = f"{alpha}{symbol}.{beta}"
                j.append(((i[0][0], new_i), i[1]))

    j = list(set(j))
    return define_closure(j, grammar)


def find_all_symbols(grammar):
    symbols = list(grammar['s_n_terminal'] + grammar['s_terminal'])
    for productions in grammar['producoes'].values():
        for production in productions:
            for c in production:
                if c not in symbols:
                    symbols.append(c)

    return list(symbols)


def find_eqivalent_item(symbol, item, items):
    for i, t  in items.items():
        i_name, i_symbol = list(t.keys())[0]
        if i_symbol == symbol:
            i_item = t[(i_name, i_symbol)]
            if i_item == item:
                return i

    return None


def search_items(grammar):
    #((cabeça, corpo), terminal/$)
    closer_i0 = define_closure([(("S'", ".S"), "$")], grammar)
    items = {
        'I0': {("->", "$") : closer_i0}
    }
    symbols = find_all_symbols(grammar)
    aux_i = 1
    analise_index = 0

    while True:
        add_new_item = False
        for item in list(items[f"I{analise_index}"].values()):
            for symbol in symbols:
                goto_item_symbol = define_goto(item, symbol, grammar)

                equivalent_item  = find_eqivalent_item(symbol, goto_item_symbol, items)
                if goto_item_symbol and not equivalent_item:#(goto_item_symbol not in items.values()):
                    add_new_item = True
                    items[f"I{aux_i}"] = {(f"I{analise_index}", symbol): goto_item_symbol}
                    aux_i += 1
                elif equivalent_item:
                    add_new_item = True
                    key = list(items[f"{equivalent_item}"].keys())[0]
                    origin = key[0]
                    new_origin = f"{origin}_I{analise_index}"
                    value = items[f"{equivalent_item}"][key]
                    items[f"{equivalent_item}"] = {
                        (new_origin, key[1]): value
                    }

        analise_index += 1
        if analise_index >= aux_i:
            break

    items_s = {key: {str(k): v for k, v in val.items()} for key, val in
            items.items()}
    print(json.dumps(items_s, indent=4))
    #print(analise_index)

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
