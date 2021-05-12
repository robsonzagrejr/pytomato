import json
import pytomato.gramatica_lc as glc


if __name__ == "__main__":
    #"d > c"
    grammar_text = f"""
S'->S
S->CC
C->cC | d
    """
    print
    grammar_dict = glc.texto_para_obj(grammar_text, 'GLC_Test')
    print(grammar_dict)
    g_glc = glc.define_components(grammar_dict)
    #print(json.dumps(g_glc, indent=4))

