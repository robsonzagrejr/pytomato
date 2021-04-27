class AF:
    """
        Classe usada para representar um Autômato Finito

        Attributes
        ----------
        n_states: int
            Número de estados.
        start_state: str
            Estado inicial.
        accept_states: list
            Lista contendo os estados de aceitação.
        alphabet: list
            Lista contendo os símbolos do alfabeto.
        transition_table: dict
            Dicionário de dicionários, no qual cada par chave-valor emula uma linha na tabela de transições.
        is_AFND: bool
            Diz se o AF é não determinístico.
        states: list
            Lista contendo os nomes de todos os estados do AF.

        Methods
        -------
        write_to_file(str=filename)
            Escreve o objeto em um arquivo de nome 'filename'
        string_in_file_format()
            Retorna o objeto codificado em uma string seguindo o formato de arquivo '.jff'
        get_states_as_viz_nodes()
            Retorna os estados em uma lista de dicionários({id, label})
        get_transitions_as_viz_edges()
            Retorna as transições em uma lista de dicionários({from, to, label})
        determinize()
            Determiniza o AF caso o mesmo seja um AFND
        determinize_with_epsilon()
            Determiniza o AF se o mesmo for um AFND com &-transições
        determinize_without_epsilon()
            Determiniza o AF se o mesmo for um AFND sem &-transições
        define_new_states()
            Define novos estados para o AF se baseando em uma lista passada como parâmetro.
        calculate_epsilon_set()
            Retorna um dicionário de lista que simula a função &-fecho para cada estado do AF
        recognize(str=word)
            Retorna true se a palavra 'word' é reconhecida pelo AF, ou false caso contrário
        get_name(str=state_list)
            Retorna um novo nome para o conjunto de estados da entrada
        remove_from_transition_table(states)
            Remove a lista de estados 'states' da tabela de transição
        remove_unreachable_states()
            Remove estados inalcançaveis do automato
        remove_dead_states()
            Remove estados mortos do automato
        recreate_states(equi_classes)
            Recria o AF a partir da lista de estados 'equi_classes' que são as novas classes de equivalência
        remove_equivalent()
            Remove classes de equivalência do AF utilizando o método de Hopcroft
        minimize_af()
            Método central que chama os demais métodos para a completa minimização do AFD
        set_alphabet()
            Método que utiliza o alfabeto passado como parametro para alterar manualmente o alfabeto do AF
        set_n_states()
            Método que utiliza o numero passado como parametro para alterar manualmente o numero de estados do AF
        set_states()
            Método que utiliza a lista de estados passada como parametro para alterar manualmente a lista de estados do AF
        set_start_states()
            Método que utiliza o estado passado como parametro para alterar manualmente o estados inicial do AF
        set_accept_states()
            Método que utiliza a lista de estados de aceitação passada como parametro para alterar manualmente a lista de
             estados de aceitação do AF
        set_transitions()
            Método que utiliza o dicionário passado como parametro para alterar manualmente a tabela de transições do AF
        """
    ERRO_1 = "O número de estados deve ser inteiro e maior que 0.(linha 1)"
    ERRO_2 = "Não há estado inicial.(linha 2)"
    ERRO_3 = "Não pode haver mais de um estado inicial.(linha 2)"
    ERRO_4 = "Por questões de legibilidade, nomes de estados não podem ser símbolos do alfabeto.(linha "
    ERRO_5 = "Se presentes, as linhas de transição devem conter 3 elementos separados por \",\".(linha "
    ERRO_6_1 = "O símbolo \""
    ERRO_6_2 = "\" não pertence ao alfabeto definido.(linha "

    #def __init__(self, meta_data, transitions):
    def __init__(self, meta_data, transitions, n_states=0, start_state='', accept_states=None, alphabet=None, transition_table=None, is_afnd=False, states=None):
        """
        :param meta_data: list
            lista contendo, NA SEGUINTE ORDEM: número de estados, estado inicial, estados de aceitação, alfabeto.
        :param transitions: list
            tabela de transição.
        :raise Exception:
            erro referente a falha no processo de leitura das informações do AF
        """

        # constrói AF com informações obtidas de maneira externa, caso states n seja None, ou um AF com valores padrão
        if states is not None or (meta_data is None and transitions is None):
            self.n_states = n_states
            self.start_state = start_state
            self.accept_states = accept_states
            self.alphabet = alphabet
            self.transition_table = transition_table
            self.is_afnd = is_afnd
            self.states = states
            return

        # lê o numero de estados
        try:
            self.n_states = int(meta_data[0])
            if self.n_states <= 0:
                raise Exception(self.ERRO_1)
        except ValueError:
            raise Exception(self.ERRO_1)
        # NOTA: Estados e símbolos sempre são salvos como strings
        # verifica se há apenas um estado inicial
        start_state = str(meta_data[1])
        if start_state == "":
            raise Exception(self.ERRO_2)
        if ',' in start_state:
            raise Exception(self.ERRO_3)
        self.start_state = start_state
        # cria a lista de estados de aceitação
        self.accept_states = [str(state) for state in meta_data[2].split(",")]
        # cria a lista contendo os símbolos do alfabeto
        self.alphabet = [str(symbol) for symbol in meta_data[3].split(",")]
        if self.start_state in self.alphabet:
            print(self.start_state)
            raise Exception(self.ERRO_4 + "2)")
        for state in self.accept_states:
            if state in self.alphabet:
                raise Exception(self.ERRO_4 + "3)")
        # se '&' 'pertencer' ao alfabeto, esse AF é um AFND
        self.is_afnd = "&" in self.alphabet
        # inicializa a tabela de transições com o estado inicial e os estados de aceitação
        self.transition_table = {self.start_state: dict()}
        for state in self.accept_states:
            self.transition_table.update({state: dict()})
        # adiciona as transições definidas a partir da linha 5 a tabela de transições
        for transition in transitions:
            # ignora linhas vazias
            if transition == '':
                continue
            try:
                origin_state, symbol, reachable_states = [str(t) for t in transition.split(",")]
            except:
                line = str(5 + transitions.index(transition))
                raise Exception(self.ERRO_5 + line + ")")
            if symbol not in self.alphabet:
                line = str(5 + transitions.index(transition))
                raise Exception(self.ERRO_6_1 + symbol + self.ERRO_6_2 + line + ")")
            # cria a linha de 'origin_state' na tabela, se não houver
            if origin_state not in self.transition_table.keys():
                self.transition_table.update({origin_state: dict()})
            # atualiza as transições de 'origin_state'
            state_transitions_by = self.transition_table[origin_state]
            reachable_states = sorted([str(reachable_state) for reachable_state in reachable_states.split("-")])
            for state in reachable_states:
                if state in self.alphabet:
                    line = str(5 + transitions.index(transition))
                    raise Exception(self.ERRO_4 + line + ")")
            new_transition = {symbol: reachable_states}
            state_transitions_by.update(new_transition)
            self.is_afnd = self.is_afnd or len(state_transitions_by[symbol]) > 1
            # adiciona estados que ainda não pertencem a tabela de transição. Esse passo garante que eventuais estados
            # mortos sejam adicionados a tabela, o que pode ajudar na implementação futura da minimização de AF.
            for state in reachable_states:
                if state not in self.transition_table.keys():
                    self.transition_table.update({state: dict()})

        self.states = list(self.transition_table.keys())
        # atualiza o número de estados. Não reclama se for diferente.
        self.n_states = len(self.states)

    def set_alphabet(self, alphabet):
        """
        :param alphabet: list
            Lista de strings que representam o alfabeto do AF
        """
        self.alphabet = alphabet

    def set_transistions(self, transitions):
        """
        :param transitions: dicionário
           Dicionário no padrão adotado para representar as linhas da tabela de transições do AF
        """
        self.transition_table = transitions
        self.states = list(self.transition_table.keys())

    def set_final_states(self, final_states):
        """
        :param final_states: list
           Lista de string com os nomes dos estados de aceitação do AF
        """
        self.accept_states = final_states
    
    def set_start_state(self, start_state):
        """
        :param start_state: string
           String do nome do estado inicial do AF
        """
        self.start_state = start_state

    def set_n_states(self, n_states):
        """
        :param n_states: int
           Inteiro que representa o número de estados do AF
        """
        self.n_states = n_states
    
    def set_is_afnd(self, is_afnd):
        """
        :param is_afnd: bool
            Bool que diz se o AF é ou n um AFND
        """
        self.is_afnd = is_afnd

    def __str__(self):
        """
        :return: str com a representação dos dados do objeto; NÃO segue o padrão dos arquivos '.jff'.
        """
        return f"Número de estados: {self.n_states}\n" \
               f"Estado Inicial: {self.start_state}\n" \
               f"Estados de aceitação: {self.accept_states}\n" \
               f"Tabela de transições: {self.transition_table}\n" \
               f"É AFND: {self.is_afnd}\n" \
               f"Nomes dos estados: {self.states}"

    def write_to_file(self, filename):
        """
        :param filename: str
            nome do arquivo no qual o af deve ser escrito.
        :return:
        """
        with open(filename, "w") as file:
            file.write(self.string_in_file_format())

    def string_in_file_format(self):
        """
        :return: str
            string representando o formato o AF seguindo o formato dos arquivos '.jff'.
        """
        transition_table_as_string = ""
        # Formata as entradas do dicionário para o formato do arquivo .jff
        for origin_state, transitions in self.transition_table.items():
            if bool(transitions):
                for symbol, destiny_states in transitions.items():
                    destiny_states_as_string = destiny_states[0]
                    if len(destiny_states) > 1:
                        for i in range(1, len(destiny_states)):
                            destiny_state = destiny_states[i]
                            destiny_states_as_string = destiny_states_as_string + f"-{destiny_state}"
                    transition_table_as_string = transition_table_as_string + \
                                                 f"{origin_state},{symbol},{destiny_states_as_string}\n"
        return f"{self.n_states}\n" \
               f"{self.start_state}\n" \
               f"{','.join(self.accept_states)}\n" \
               f"{','.join(self.alphabet)}\n" \
               f"{transition_table_as_string}"

    def get_states_as_vis_nodes(self):
        """
        :return: list
            lista de dicionários contendo os dados necessários para criar nodes no vis.
        """
        nodes = list()

        for state in self.states:
            color_options = {'border': '#004582',
                             'background': '#91D4ED'}
            state_label = state

            if state == self.start_state:
                state_label = '->' + state_label
                color_options = {'border': '#F25D00',
                                 'background': '#EEB679'}

            if state in self.accept_states:
                state_label = state_label + '*'
                color_options = {'border': '#008239',
                                 'background': '#91EDAC'}

            nodes.append({'id': self.states.index(state),
                          'label': state_label,
                          'color': color_options})
        return nodes

    def get_transitions_as_vis_edges(self):
        """
        :return: list
            lista de dicionários contendo os dados necessários para criar transições no viz.
        """
        edges_control = list()
        edges = list()
        for init_state, transitions in self.transition_table.items():
            for symbol, reachable_states in transitions.items():
                for index, state in enumerate(reachable_states):
                    factor = 0
                    if index == 0:
                        factor = 0
                    elif index % 2 == 0:
                        factor = index * 0.2
                    else:
                        factor = index * 0.2 * (-1)

                    have_ocurred = edges_control.count([state, init_state])

                    if have_ocurred > 0:
                        factor = factor + have_ocurred * 0.2

                    edges_control.append([init_state, state])

                    self.states.index(state)

                    # edges.append({
                    #     'from': init_state,
                    #     'to': state,
                    #     'label': symbol,
                    #     'smooth': {'type': 'curvedCCW', 'roundness': factor},
                    #     'color': '#6b705c'
                    # })

                    edges.append({
                        'from': self.states.index(init_state),
                        'to': self.states.index(state),
                        'label': symbol,
                        'smooth': {'type': 'curvedCCW', 'roundness': factor},
                        'color': '#6b705c'
                    })


        return edges

    def determinize(self):
        """
        :return:
        """
        if not self.is_afnd:
            pass
        if '&' in self.alphabet:
            self.determinize_with_epsilon()
        else:
            self.determinize_without_epsilon()

    def determinize_with_epsilon(self):
        """
        :return:
        """
        print('determinizando com epsilon')
        # calcula o epsilon fecho
        epsilon_set = self.calculate_epsilon_set()
        states_to_define = [epsilon_set[self.start_state]]
        # calcula as transicoes para cada estado em states_to_define, enquanto houver
        new_accept_states, new_transition_table = self.define_new_states(states_to_define, dict(), epsilon_set)
        # remove o '&' do alfabeto
        self.alphabet.remove('&')
        # mudar o conjunto de estados de aceitação
        self.accept_states = new_accept_states
        # mudar o estado inicial
        self.start_state = self.get_name(epsilon_set[self.start_state])
        # mudar a tabela de transicoes
        self.transition_table = new_transition_table
        # atualizar a lista de statos
        self.states = list(self.transition_table.keys())
        # atualizar o numero de estados
        self.n_states = len(self.states)

    def determinize_without_epsilon(self):
        """
        :return:
        """
        print('determinizando sem epsilon')
        states_to_define = []
        # primeiro percorre para obter novos estados e os adiciona em states_to_define
        for transitions in self.transition_table.values():
            new_states = [state for state in transitions.values() if len(state) > 1 and state not in states_to_define]
            if new_states:
                states_to_define.extend(new_states)
        # define todos os estados em states_to_define, e adiciona novos a lista caso necessário
        new_accept_states, _ = self.define_new_states(states_to_define, self.transition_table, dict())
        # atualiza refrencias a nomes antigos no dicionario
        for origin_state, transitions in self.transition_table.items():
            for symbol, destiny_states in transitions.items():
                if len(destiny_states) > 1:
                    self.transition_table[origin_state][symbol] = [self.get_name(destiny_states)]
        # atualizar a lista de estados de aceitação
        self.accept_states.extend(new_accept_states)
        # atualizar a lista de estados
        self.states = list(self.transition_table.keys())
        # atualizar o numero de estados
        self.n_states = len(self.states)

    def define_new_states(self, states_to_define, transition_table, epsilon_set):
        """
        :return: list
            lista contendo, na seguinte ordem: [0]conjunto de novos estados de aceitação; [1]nova tabela de transições.
        """
        new_accept_states = list()
        while states_to_define:
            new_origin_state = sorted(states_to_define.pop(0))
            new_origin_state_name = self.get_name(new_origin_state)
            is_accept_state = False
            transitions = dict()
            for symbol in self.alphabet:
                new_state = list()
                for state in new_origin_state:
                    # checa se new_origin_state é um estado de aceitação
                    if state in self.accept_states and not is_accept_state:
                        is_accept_state = True
                    if symbol in self.transition_table[state].keys():
                        # adiciona o epsilon fecho de cada estado se for AFND com &-transições
                        if '&' in self.alphabet:
                            for s in self.transition_table[state][symbol]:
                                # eventualmente pode acabar adicionando estados repetidos
                                new_state.extend(epsilon_set[s])
                            continue
                        # eventualmente pode acabar adicionando estados repetidos
                        new_state.extend(self.transition_table[state][symbol])
                if new_state:
                    # retira elementos repetidos e ordena a lista que contém os estados que compoe o novo estado
                    new_state = sorted(list(set(new_state)))
                    new_state_name = self.get_name(new_state)
                    # checar se new_state já foi definido; se não, adicioná-lo a lista para definição
                    if new_state_name not in transition_table.keys() and new_state not in states_to_define:
                        states_to_define.append(new_state)
                    # adicionar entrada a transitions
                    transitions.update({symbol: [new_state_name]})
            if is_accept_state and new_origin_state_name not in new_accept_states:
                new_accept_states.append(new_origin_state_name)
            # adicionar a nova linha à nova tabela de transição
            transition_table.update({new_origin_state_name: transitions})
        return [new_accept_states, transition_table]

    def calculate_epsilon_set(self) -> dict:
        """
        :return: dict
            dicionário de listas que simula a funcao &-fecho dos estados do AF.
        """
        epsilon_set = dict()
        for origin_state, transitions in self.transition_table.items():
            # adiciona o proprio estado ao seu &-fecho
            reachable_states = [origin_state]
            if '&' in transitions.keys():
                states_to_check = transitions['&']
                # checa todos os estados alcancaveis a partir de origin_state enquanto ouver estado em states_to_check
                while states_to_check:
                    s = states_to_check.pop(0)
                    reachable_states.append(s)
                    if '&' in self.transition_table[s].keys():
                        for state in self.transition_table[s]['&']:
                            if state not in states_to_check and state not in reachable_states:
                                states_to_check.append(state)
            epsilon_set.update({origin_state: reachable_states})
        return epsilon_set

    def recognize(self, word):
        """
        :param word: str
            Palavra que se deseja tentar reconhecer com o AF.
        :return: bool
            Se a palavra pertencer a linguagem, retorna True. Se não, retorna False.
        """
        # determiniza o automato e usa o obj resultante para tentar reconhecer a palavra 'word'
        self.determinize()
        world_len = len(word)
        actual_state = self.start_state
        # enquando a palavra não for vazia
        while word:
            # ordena a lista de symbolos pelo tamanho
            symbols = sorted(self.transition_table[actual_state].keys(), key=len)
            # percorre a lista de símbolos pelos quais é possível para transicionar, partindo do estado atual
            for symbol in symbols:
                # se a palavra começa com o símbolo 'symbol', atualiza informações
                if word.startswith(symbol):
                    # consome o símbolo do início da palavra
                    word = word.replace(symbol, "", 1)
                    # transiciona para o próximo estado
                    actual_state = self.transition_table[actual_state][symbol][0]
                    break
            # se o tamanho da palavra atual for maior que o último valor salvo atualiza a informação
            if world_len > len(word):
                world_len = len(word)
            else:
                # se não for maior o valor é igual ao último salvo, o que significa que o simbolo no inicio da palavra
                # não pertence ao alfabeto do af, e logo a palavra não pertence a linguagem
                return False

        # se o estado atual for um estado de aceitação, a palavra pertence à linguagem; se não a palavra não pertence
        if actual_state in self.accept_states:
            return True
        return False

    @staticmethod
    def get_name(states_list):
        """
        :param states_list: str
            lista de estados
        :return: string
            string contendo um novo nome para um conjunto de estados.
        """
        if len(states_list) > 1:
            return '{' + ';'.join(states_list) + '}'
        return states_list[0]

    def remove_from_transition_table(self, states):
        """
        :return:
        """
        # retira linhas as linhas referentes aos estados da tabela
        for state in states:
            # retira da lista de estados de aceitação, se for o caso
            if state in self.accept_states:
                self.accept_states.remove(state)
            self.transition_table.pop(state)
        # retira transições de outros estados para esse
        for origin_state in self.transition_table.keys():
            # simbolos pelos quais é posivel transitar
            symbols = list(self.transition_table[origin_state].keys())
            for symbol in symbols:
                original_destiny_states = self.transition_table[origin_state][symbol]
                # nova lista de estados alcançáveis(diferença entre a lista existente e a de estados sendo apagados)
                new_destiny_states = list(set(original_destiny_states).difference(set(states)))
                # se após a retirada dos estados da lista states ainda existir alguma transição por symbol, atualiza;
                if new_destiny_states:
                    self.transition_table[origin_state].update({symbol: new_destiny_states})
                    continue
                # caso nao, remove as transicoes por symbol
                self.transition_table[origin_state].pop(symbol)
        # atualiza lista de estados
        self.states = list(self.transition_table.keys())
        self.n_states = len(self.transition_table.keys())

    def remove_unreachable_states(self):
        """
        :return:
        """
        # calcula estados de aceitacao
        reachable_states = list()
        states_to_visit = [self.start_state]
        # Adiciona a lista reachable states estados alcançaveis, começando pelo estado inicial
        while states_to_visit:
            origin_state = states_to_visit.pop()
            reachable_states.append(origin_state)

            for _, states in self.transition_table[origin_state].items():
                for state in states:
                    if state not in states_to_visit and state not in reachable_states:
                        states_to_visit.append(state)

        # remove referencias a estados inalcançáveis na tabela de transicao e atualiza lista de estados, estados de acei
        # tacao
        self.remove_from_transition_table(set(self.states).difference(set(reachable_states)))

    def remove_dead_states(self):
        """
        :return:
        """
        live_states = set()
        states_to_visit = list()
        # Marca estados com transições para os estados finais
        for state in self.states:
            for _, states in self.transition_table[state].items():
                for _state in states:
                    if _state in self.accept_states:
                        states_to_visit.append(state)

        # Marca o resto dos estados por rastreação
        while states_to_visit:
            origin_state = states_to_visit.pop()
            live_states.update(origin_state)

            for state in self.states:
                for _, states in self.transition_table[state].items():
                    for _state in states:
                        if _state == origin_state and state not in live_states:
                            states_to_visit.append(state)
        # Remove referencias dos estados mortos na tabela de transição e atualiza os estados
        self.remove_from_transition_table(set(self.states).difference(set(live_states)))

    def recreate_states(self, equi_classes):
        """
        :return:
        """
        new_accept_states = []
        new_start_state = None
        # A partir das novas classes de equivalencia, atribui aos novos atributos do AF
        for equi_class in equi_classes:
            if self.start_state in equi_class:
                # Novo estado inicial
                new_start_state = self.get_name(equi_class)
            for final_state in self.accept_states:
                if final_state in equi_class and self.get_name(equi_class) not in new_accept_states:
                    # Novo estado de aceitação
                    new_accept_states.append(self.get_name(equi_class))

        # Nova tabela de transição
        transitions = {}
        for equi_class in equi_classes:
            first_state = equi_class[0]
            state_name = self.get_name(equi_class)
            transitions[state_name] = {}
            # define os estados para os quais o novo estado deve transicionar, baseado nas classes de equivalencia dos
            # estados alcançados por um estado(primeiro) dessa classe de equivalencia. Esse estado é o first_state
            for symbol in self.alphabet:
                # checa se o estado possui transições pelo simbolo symbol
                if symbol in self.transition_table[first_state].keys():
                    # pega o estado alcancado, através de symbol, partindo de first_state
                    destiny_state = self.transition_table[first_state][symbol][0];
                    # procura a classe de equivalencia do estado
                    for equi_class_ in equi_classes:
                        if destiny_state in equi_class_:
                            # adiciona o estado a linha da tabela de trans desse estado
                            transitions[state_name][symbol] = [self.get_name(equi_class_)]
        # Atribui os novos valores para o AF
        self.start_state = new_start_state
        self.accept_states = new_accept_states
        self.transition_table = transitions
        self.states = list(self.transition_table.keys())

    def remove_equivalent(self):
        """
        :return:
        """
        p_classes = [self.accept_states, list(set(self.states).difference(set(self.accept_states)))]

        new_p_class_created = True
        # continuara enquanto novas classes forem definidas
        while new_p_class_created:
            new_p_class_created = False

            # tentara quebrar todas as p_classes por um simbolo por vez
            for symbol in self.alphabet:
                p_classes_aux = list()
                for p_class in p_classes:
                    # se for 1 já e minimo
                    if len(p_class) == 1:
                        p_classes_aux.append(p_class)
                        continue
                    # lista que representa a p_class que está sendo verificada
                    p_class_aux = list()
                    # lista que representa a nova p_class q pode surgir
                    new_p_class_aux = list()
                    # estado que será usado como pivo(num sei escrever)
                    pivot = p_class[0]

                    if symbol in self.transition_table[pivot].keys():
                        # pivot tem transições por symbol
                        # estado alcançado transicionando pelo simbolo symbol a partir do estado pivot
                        pivot_destiny = self.transition_table[pivot][symbol][0]
                        # pega a classe de equivalencia do estado destino de pivot
                        pivot_destiny_equivalence_state = [p for p in p_classes if pivot_destiny in p][0]
                    else:
                        # pivot n tem transicoes por symbol
                        pivot_destiny_equivalence_state = []

                    # para cada estado q n é o pivot
                    for state_to_check in p_class:
                        # se for o pivot ignora
                        if state_to_check == pivot:
                            p_class_aux.append(state_to_check)
                            continue

                        # se state_to_check não tiver transições por symbol
                        if symbol not in self.transition_table[state_to_check].keys():
                            # se pivot tb n tiver transições por symbol, ok;
                            if not pivot_destiny_equivalence_state:
                                p_class_aux.append(state_to_check)
                                continue
                            else:
                                # caso contrario, adiciona a new_p_class
                                new_p_class_aux.append(state_to_check)
                                new_p_class_created = True
                            continue

                        # se tiver, pega o estado alcançavel por state_to_check
                        state_destiny = self.transition_table[state_to_check][symbol][0]

                        # verifica se esta na mesma classe do estado alcançado por pivot; se n estiver adiciona a
                        # new_p_class
                        if state_destiny not in pivot_destiny_equivalence_state:
                            new_p_class_aux.append(state_to_check)
                            new_p_class_created = True
                            continue
                        p_class_aux.append(state_to_check)

                    p_classes_aux.append(p_class_aux)
                    # se new_p_class n for nulo, significa q uma nova p_class surgiu, e deve ser adicionada a p_classes
                    if new_p_class_aux:
                        p_classes_aux.append(new_p_class_aux)
                # adiciona novas classes antes de tentar minimizar pelo proximo simbolo
                p_classes = p_classes_aux
        self.recreate_states(p_classes)

    def minimize_af(self):
        """
        :return:
        """
        print(self.__str__())
        # determiniza o AFD para o funcionamento do hopcroft
        self.determinize()
        # Remove unreachble states
        self.remove_unreachable_states()
        # Remove dead states
        self.remove_dead_states()
        # Remove equivalent states and recreate AFD
        self.remove_equivalent()
        print(self.__str__())
