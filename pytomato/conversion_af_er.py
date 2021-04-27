class Node:
    def __init__(self, left=None,right=None,data=None,father=None,first=None,fulfilled=None):
        self.left = left
        self.right = right
        self.data = data
        self.father = father
        self.is_first_of_chain = first
        self.fulfilled = fulfilled

        self.lastpos = None
        self.firstpos = None
        self.nullable = None

    def post_order(self, root):
        res = []
        if root:
            res = self.post_order(root.left)
            res = res + self.post_order(root.right)
            res.append(root)
        return res


def render_tree(er):
    string = er.replace(' ','')[::-1]
    tree = Node()
    last = tree
    idx = 0
    while(idx < len(string)):
        char = string[idx]
        if char == '#':
            last.data = '#'
            last.father = Node(left=last)
            last.is_first_of_chain = True
            tree = last
        else:
            last, idx = add_node(idx,string,last)
        idx = idx+1
    return tree.father.left

def add_node(idx, string, node):
    char = string[idx]
    
    if idx+1 < len(string) and string[idx+1] == '\\':
        idx += 1
        new = concat(Node(data=char),node)
        return new.left, idx

    if char == ')':
        idx = idx+1
        char = string[idx]
        new_node = Node(data=char, first=True)
        new_node.father = Node(left=new_node)
        while(not string[idx] == '('):
            new_node, idx = add_node(idx+1, string, new_node)

        n = new_node
        while(n.data):
            n = n.father
        n = n.left
        if not node.data == '*':
            new = concat(n,node)
            new.left.fulfilled = True
            return new.left, idx
        else:
            node.left = n
            node.father.fulfilled = True
            return node.father, idx

    if char == '(':
        return node, idx

    if char == '|':
        n = node
        while(not n.is_first_of_chain):
            n = node.father
        new = Node(right=n,data='|', father=n.father)
        n.father.left = new
        n.father = new
        return new, idx

    if node.fulfilled:
        new = concat(Node(data=char),node)
        return new.left, idx

    if node.data == '|':
        node.left = Node(data=char, first=True, father=node)
        return node.left, idx
        
    if node.data == '*':
        node.left = Node(data=char,father=node)
        node.fulfilled = True
        return node, idx

    new = concat(Node(data=char),node)
    return new.left, idx
    
def concat(node1,node2):
    if node2.is_first_of_chain:
        is_first = True
        node2.is_first_of_chain = False
    else:
        is_first = False
    new = Node(right=node2, data='concat', father=node2.father, first=is_first)
    node1.father = new
    node2.father.left = new
    new.left = node1
    return new

def define_nodes(tree):
    nodes = tree.post_order(tree)
    count = 1
    nodes_idx = dict()
    for n in nodes:

        if n.data == '|':
                n.nullable = n.left.nullable or n.right.nullable
                n.firstpos = n.left.firstpos | n.right.firstpos
                n.lastpos = n.left.lastpos | n.right.lastpos

        elif n.data == 'concat':
            n.nullable = n.left.nullable and n.right.nullable
            
            if n.left.nullable:
                n.firstpos = n.left.firstpos | n.right.firstpos
            else:
                n.firstpos = n.left.firstpos

            if n.right.nullable:
                n.lastpos = n.left.lastpos | n.right.lastpos
            else:
                n.lastpos = n.right.lastpos
            
        elif n.data == '*':
            n.nullable = True
            n.firstpos = n.left.firstpos
            n.lastpos = n.left.lastpos

        else:
            if n.data == '&':
                n.nullable = True
                n.firstpos = set()
                n.lastpos = set()
            else:
                n.nullable = False
                n.firstpos = set([count])
                n.lastpos = set([count])
                nodes_idx[f'{count}'] = n.data
                count = count + 1

    return count-1, nodes_idx

def define_followpos(tree, n_nodes):
    nodes = tree.post_order(tree)
    followpos = dict()
    for idx in range(n_nodes):
        followpos[f'{idx+1}'] = set()

    for n in nodes:

        if n.data == 'concat':
            for lastpos_node in n.left.lastpos:
                followpos[str(lastpos_node)] = followpos[str(lastpos_node)] | n.right.firstpos
        if n.data == '*':
            for firstpos_node in n.lastpos:
                followpos[str(firstpos_node)] = followpos[str(firstpos_node)] | n.firstpos

    return followpos, tree.firstpos

def afd(followpos, nodes_idx, initial_state):
    union = dict()
    states = list()
    states.append(initial_state)
    visited_states = list()
    automata = dict()
    
    while(not len(states) == 0):
        state = states.pop()
        visited_states.append(state)
        for pos in state:
            node = nodes_idx.get(str(pos))
            if not node == '#':
                if not union.__contains__(node):
                    union[node] = set(followpos.get(str(pos)))
                else:
                    union[node] = union.get(node) | set(followpos.get(str(pos)))

        for s in union.items():
            if visited_states.count(s[1]) == 0:
                states.append(s[1])

        automata[str(state)] = union.copy()
        union.clear()

    return automata

def format_afd(automata, initial_state, final, alphabet):
    initial_state = [str(i) for i in initial_state]
    afd = dict()
    afd['n_estados'] = len(automata)
    afd['inicial'] = "{"  + ', '.join(initial_state) + "}"
    afd['aceitacao'] = list()
    afd['alfabeto'] = list(alphabet)
    afd['transicoes'] = dict()

    for transiction in automata:
        if transiction.find(final) >= 0:
            afd.get('aceitacao').append(transiction)
        t = dict()
        for a in alphabet:
            tr = automata.get(transiction).get(a)
            if (tr):
                t[a] = [str(tr)]
            #else:
            #    t[a] = []
        afd.get('transicoes')[transiction] = t
        
    return afd

letters = 'abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'

def transform_suffix(suffix):
    string = ''
    is_until = False
    for c in suffix:
        if c == '-':
            is_until = True
        else:
            if is_until:
                if c.isnumeric():
                    s = numbers.split(string[-1])[1]
                else:
                    if c.isupper():
                        s = letters.upper().split(string[-1])[1]
                    else:
                        s = letters.split(string[-1])[1]
                string += s.split(c)[0] + c
                is_until = False
            else:
                string += c

    str_ref = ''
    for c in string:
        str_ref += c + '|'

    return '(' + str_ref[0:-1] + ')'
    
def refatorate_regex(string):
    preffix = ''
    is_bracket = False
    for c in string:
        if c == '[':
            is_bracket = True
            suffix = ''
        elif c == ']':
            is_bracket = False
            preffix += transform_suffix(suffix)
        else:
            if is_bracket:
                suffix += c
            else:
                preffix += c

    return preffix + '#'

def er_to_afd(string):
    string = refatorate_regex(string)
    tree = render_tree(string)
    n_nodes, nodes_idx = define_nodes(tree)
    followpos, initial_state = define_followpos(tree, n_nodes)
    automata = afd(followpos,nodes_idx,initial_state)

    final = [item[0] for item in list(nodes_idx.items()) if item[1] == '#'][0]
    alphabet = set([item[1] for item in list(nodes_idx.items()) if not item[1] == '#'])

    return format_afd(automata, initial_state, final, alphabet)



"""Teste
Main criado para testar as funções.
"""
if __name__ == '__main__':
    er_to_afd('[J-M1-9]*')
    # er_to_afd('a(a|b)*a')
    # er_to_afd('aa*(bb*aa*b)*')

