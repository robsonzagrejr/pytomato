# Projeto de Linguagens Formais
pytomato - Sistema Interativo de Linguagens Formais e Compiladores

## 1. Integrantes do Grupo

1. Gabriel Rosa Costa Giacomoni Pes
2. Cainã Correa Caldas
3. Felipe Longarai Trisotto
4. Robson Zagre Junior
5. Sofia Regis
6. Caetano Colin Torres

## 2. Visão Geral

- Instâncias serão salvas no navegador.
- Na caixa de texto serão inseridos os autômatos/gramáticas em formato texto seguindo as sintaxes apresentadas na Seção 3.
- O programa converte texto em estruturas de dados/objetos internamente.
- Funcionalidade de Download/Upload de autômatos e gramáticas.
- Nomes dos objetos personalizáveis
- Após o Upload ou a inserção via texto de um autômato/gramática no sistema, ele ficará disponível para download e visualização a qualquer momento.

## 3. Sintaxe

### 3.1. Autômato em Texto

Os autômatos no pytomato serão representados seguindo a seguinte sintaxe:

```
n_de_estados
estado_inicial
estados_de_aceitacao
alfabeto
transicao_1
transicao_2
transicao_3
transicao_4
transicao_5
.
.
.
.
.
transicao_n
```

#### 3.1.2. Exemplo de Autômato em Tabela/Texto

. | a | b
------------ | ------------- | -------------
->0 | 1 | 2 
*1 | 1 | 3 
*2 | 4 | 2 
3 | 1 | 3 
4 | 4 | 2 

O autômato acima convertido para texto seguindo a sintaxe:

```
5
0
1,2
a,b
0,a,1
0,b,2
1,a,1
1,b,3
2,a,4
2,b,2
3,a,1
3,b,3
4,a,4
4,b,2
```

### 3.2. Gramática em Texto

As gramáticas no pytomato serão representadas seguindo a seguinte sintaxe:

```
simbolo_inicial -> prod1 | prod2 | prod3
1_esimo_simbolo -> prod1 | ... | prod2
.
.
.
.
.
n_esimo_simbolo -> prod1 | ... | prod2
```

#### 3.1.2. Exemplo de Gramática em Texto

Exemplo prático de como escrever uma gramática no pytomato:

```
S -> aA | a | &
A -> bA | a
```

## 4. Instalação

Optamos por usar a framework *Dash* (Componentes HTML em classes python), biblioteca para buildar apps web usando código em Python.

>Requisitos: poetry, python3 e makefile.

```
make install
```

## 5. Execução

Para executar o app digite:
```
make app
```

Entre no seu navegador e digite **http://0.0.0.0:8080/** como URL.

Caso tenha problema de versionamento com o python, outra forma de instanciar o servidor é via docker:

```
docker-compose up -d
```

Com isso, é possível também alterar a porta na qual o servidor vai ser acessado, basta alterar com a porta de sua preferência no arquivo *docker-compose.yml*:

```yml
ports:
    - "PORTA:8080" 
```

Entre no seu navegador e digite **http://0.0.0.0:`PORTA`/** como URL.
## 6. Organização Do Código

No diretório **./pytomato/** temos os métodos de conversão de gramáticas e autômatos (.txt para instâncias de objetos/estruturas de dados e vice-versa).

No diretório **./pages/** temos as diferentes páginas para os diferentes componentes (autômatos e gramáticas) no sistema, com seus layouts e callbacks.

No diretório **./core/** encontra-se o código principal da página web, responsável pela navegação.

*app.py* define o servidor usando bootstrap.


Cada página terá seus callbacks (dash) fazem a interface entre entradas e saídas e as funções.

## 7. Passo-a-Passo

### 7.1. Gramática - Inserção via texto no sistema.

1. Coloque o nome da sua gramática em "Gramatica label"
2. Na caixa de texto digite a gramática seguindo a sintaxe definida na seção 3.
3. Depois da inserção da gramática no sistema, ela ficará disponível para download e acesso.

### 7.2. Autômato - Inserção via texto no sistema.

1. Coloque o nome do seu autômato em "Automato label"
2. Na caixa de texto digite o autômato seguindo a sintaxe definida na seção 3.
3. Após a inserção do autômato no sistema, é possivel a visualização dele em tabela a qualquer momento.

## 8. Referências

* https://dash-bootstrap-components.opensource.faculty.ai/docs/
* https://dash.plotly.com/dash-core-components/input
