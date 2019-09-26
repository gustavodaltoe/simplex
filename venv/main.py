# INIT - FUNÇOES DE ABERTURA E FECHAMENTO DE ARQUIVO
openFile = lambda name, mode: open(name, mode)
closeFile = lambda file: file.close()
# END - FUNÇOES DE ABERTURA E FECHAMENTO DE ARQUIVO

# NOME DO ARQUIVO DE ENTRADA
FILENAME = 'entrada.txt'

# INIT - COLETANDO LINHAS DO ARQUIVO DE ENTRADA
file = openFile(FILENAME, 'r')
fileLines = file.readlines()
closeFile(file)
# END - COLETANDO LINHAS DO ARQUIVO DE ENTRADA

strToFloat = lambda str: float(str)

# INIT - FUNÇÕES DE MANIPULAÇÃO DO ARQUIVO PARA MATRIZ
lineToArray = lambda line: list(map(int, line.replace('\n', '').split(' ')))
fileToArray = lambda fileLines: list(map(lineToArray, fileLines))
# INIT - FUNÇÕES DE MANIPULAÇÃO DO ARQUIVO PARA MATRIZ

# TRANSFORMANDO TODOS OS VALORES EM UMA MATRIZ
values = fileToArray(fileLines)
objetiva = values[0]
rest = values[1:]

# EXIBINDO FUNÇÃO OBJETIVA
print('\nFUNÇÃO OBJETIVA:')
print(f'Z = {objetiva[0]} X1 + {objetiva[1]} X2')

# LISTANDO AS RESTRIÇÕES
print('\nRESTRIÇÕES:')
for r in rest:
    print(f'{r[0]} X1 + {r[1]} X2 + 1 X{rest.index(r) + 3} <= {r[2]}')

# QUANTIDADE DE COLUNAS (X1,X2,X3, ... , Xn)
QTD_COLUNAS = len(values) - 1 + 2
print(f'Xi >= 0, i = 1...{QTD_COLUNAS}')

# CONSTROI UMA MATRIZ COM A ESTRUTURA DA TABELA DO SIMPLEX
def buildSimplex(funcObjetiva, restricoes):
    # INICIALIZANDO A TABELA
    tbl = []
    # CONTAGEM PARA GUARDAR A POSIÇÃO DE ONDE SERÁ INSERIDO 1 PARA X3,X4,X5...
    cont = 2
    # PARA CADA RESTRIÇÃO, FORMAMOS UMA LINHA NA TABELA
    for rest in restricoes:
        # INICIALIZO A LINHA COM X1 E X2
        line = [rest[0], rest[1]]
        for i in range(2, QTD_COLUNAS):
            # EXEMPLO:
            #   CONT -> 2 E I -> 2:
            #       PORTANTO, X3 = 1
            if cont == i:
                line.append(1)
            else:
                line.append(0)
        # ADICIONO 1 NA CONTAGEM PARA O PROXIMO X DA PROXIMA LINHA SER = 1
        cont += 1
        # ADICIONO NO FINAL DA LINHA O VALOR LIMITE
        line.append(rest[2])
        # INSERINDO A LINHA NA TABELA
        tbl.append(line)
    print(tbl)

buildSimplex(0, rest)







