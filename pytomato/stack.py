class Stack:
    """ Implementação de estrutura de Pilha """

    def __init__(self):
        self.__stack = []

    """ Adiciona o valor ao topo da pilha """
    def push(self, value):
        self.__stack.append(value)

    """ Remove o valor no topo da pilha """
    def pop(self):
        return self.__stack.pop()

    """ Retorna o topo da pila """
    def top(self):
        return self.__stack[len(self.__stack)-1]

    """ Verifica se pilha está vazia """
    def empty(self): 
        return len(self.__stack) == 0