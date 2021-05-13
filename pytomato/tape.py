from copy import deepcopy

class Tape:
	""" Implementação de estrutura de Fita """
    
    def __init__(self, empty, tape_alphabet, content=[]):
        self.position = 0 # posicao atual da fita
        self.empty_symbol = empty
        self.alphabet = tape_alphabet
        self.content = content

    """ Moviementação do cabeçote sobre a fita """
    def move_head(self, movement):
        if movement == 'L': 
            self.move_left()
        elif movement == 'R':
            self.move_right()
        elif movement == 'S':
            pass
        else:
            pass

    """ Move o cabeçote para esquerda """
    def move_left(self):
        if self.position > 0: # se existir espaco pra esquerda, move a esquerda
            self.position -= 1
        else: # se nao, adiciona um espaço no inicio da fita e ordena como 0
            self.content.insert(0,self.empty_symbol)

    """ Move o cabeçote para direita """
    def move_right(self): 
        if self.position < len(self.content)-1: # se existir espaço a direita, vai para a direita
            self.position += 1
        else: # se nao, coloca um espaco em na fita e vai para a direita
            empty = self.empty_symbol
            self.content.append(empty)
            self.position += 1

    """ Retorna o conteudo da fita na posição do cabeçote """
    def get_content(self):
        if len(self.content) == 0:
            return self.empty_symbol
        else:
            return self.content[self.position]

    """ Inseri um conteudo na fita na posição do cabeçote """
    def set_content(self, symbol):
        if len(self.content) == 0:
            self.content.append(symbol)
        else:
            self.content[self.position] = symbol 