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
print('Z = {x1} X1 + {x2} X2'
      .format(x1 = objetiva[0], x2 = objetiva[1]))

# LISTANDO AS RESTRIÇÕES
print('\nRESTRIÇÕES:')
for r in rest:
    print('{x1} X1 + {x2} X2 + 1 X{xi} <= {tot}'
          .format(x1 = r[0], x2 = r[1], xi = rest.index(r) + 3, tot = r[2]))

# QUANTIDADE DE COLUNAS (X1,X2,X3, ... , Xn)
QTD_COLUNAS = len(values) - 1 + 2
print('Xi >= 0, i = 1...{i}'.format(i = QTD_COLUNAS))

# EXIBINDO A TABELA DE FORMA MAIS BONITINHA
def printSimplex(tbl):
    for linha in tbl:
        print('|', end='')
        for col in linha:
            print('', '%#6.2G' % col, '|', end='')
        print('')

# CONSTROI UMA MATRIZ COM A ESTRUTURA DA TABELA DO SIMPLEX
def buildSimplex(funcObjetiva, restricoes):
    # INICIALIZANDO A TABELA
    tbl = []
    # CONTAGEM PARA GUARDAR A POSIÇÃO DE ONDE SERÁ INSERIDO 1 PARA X3,X4,X5...
    cont = 2
    # PARA CADA RESTRIÇÃO, FORMAMOS UMA LINHA NA TABELA
    for rest in restricoes:
        # INICIALIZO A LINHA COM X1 E X2
        line = [rest[0] * 1.0, rest[1] * 1.0]
        for i in range(2, QTD_COLUNAS):
            # EXEMPLO:
            #   CONT -> 2 E I -> 2:
            #       PORTANTO, X3 = 1
            if cont == i:
                line.append(1.0)
            else:
                line.append(0.0)
        # ADICIONO 1 NA CONTAGEM PARA O PROXIMO X DA PROXIMA LINHA SER = 1
        cont += 1
        # ADICIONO NO FINAL DA LINHA O VALOR LIMITE
        line.append(rest[2] * 1.0)
        # INSERINDO A LINHA NA TABELA
        tbl.append(line)

    finalLine = []
    for i in range(0, QTD_COLUNAS + 1):
        if i < 2:
            finalLine.append(float(funcObjetiva[i] * -1 if funcObjetiva[i] > 0 else funcObjetiva[i]))
        else:
            finalLine.append(0.0)

    tbl.append(finalLine)

    return tbl

def temNegativo(linhaObjectiva):
    for num in linhaObjectiva:
        if num < 0:
            return True
    return False


# AQUI COMEÇA PRA VALER!!

# PRIMEIRA TABELA:
table = buildSimplex(objetiva, rest)
print('\n')
print("tabela 1:")
printSimplex(table)

zLine = len(table) - 1
# INICIALIZO UM ARRAY DE DICIONARIOS PARA SALVAR AS LINHAS QUE JÁ RESOLVI
linhasResolvidas = [
    {
        'x': 'X{cont}'.format(cont =  i + 3),
        'solved': False
     }
    for i in range(zLine)
]

# ENQUANTO EXISTE NUMERO NEGATIVO NA FUNÇÃO OBJETIVA, ENTÃO EXECUTO
qtdTabelas = 1  # CONTADOR DE VEZES QUE EXIBO A TABELA
while(temNegativo(table[zLine])):
    # INIT - ENCONTRAR A COLUNA PIVOT
    colPivot = {
        "indice": -1,
        "value": 0
    }
    for i in range(0, QTD_COLUNAS - 2):
        num = table[zLine][i]
        if (num < colPivot['value']):
            colPivot['value'] = table[zLine][i]
            colPivot['indice'] = i
    # END - ENCONTRAR A COLUNA PIVOT

    # INIT - ENCONTRAR A LINHA QUE SAI
    linPivot = {
        "indice": -1,
        "relacao": 0
    }
    for i in range(zLine):
        linha = table[i]
        b = linha[QTD_COLUNAS]
        xCol = linha[colPivot['indice']]

        # SE ESSA LINHA JA FOI RESOLVIDA, PULO
        # SE O X FOR IGUAL A 0, O RESULTADO É INDETERMINADO, ENTAO PULO
        if linhasResolvidas[i]['solved'] or xCol == 0:
            continue

        relacao = b / xCol

        if (linPivot['indice'] == -1):
            linPivot['indice'] = i
            linPivot['relacao'] = relacao
        else:
            if (relacao < linPivot['relacao']):
                linPivot['indice'] = i
                linPivot['relacao'] = relacao
    # END - ENCONTRAR A LINHA QUE SAI

    # DIVIDINDO A LINHA PIVOT PELO NUMERO ENCONTRADO
    pivot = table[linPivot['indice']][colPivot['indice']]
    for i in range(QTD_COLUNAS + 1):
        table[linPivot['indice']][i] /= pivot

    # DIZENDO QUE ESSA LINHA JÁ ESTÁ RESOLVIDA
    linhasResolvidas[linPivot['indice']]['solved'] = True
    linhasResolvidas[linPivot['indice']]['x'] = 'X{i}'.format(i = colPivot['indice'] + 1)

    # ZERANDO ESSA COLUNA E REALIZANDO AS OPERAÇÕES NA LINHA, MENOS A LINHA PIVOT
    pivot = table[linPivot['indice']][colPivot['indice']] #VAI SER IGUAL A 1 SEMPRE AGORA
    for i in range(zLine + 1):
        x = table[i][colPivot['indice']]
        if (x == 0 or i == linPivot['indice']):
            continue
        for j in range(QTD_COLUNAS + 1):
            table[i][j] -= x * table[linPivot['indice']][j]

    # EXIBINDO A TABELA
    qtdTabelas += 1
    print("\nTabela {x}:".format(x = qtdTabelas))
    printSimplex(table)

# FINALMENTE, RESULTADOS
print('\nResultados:')
z = table[zLine][QTD_COLUNAS]
for i in range(zLine):
    print('{x} = {result}'.format(x = linhasResolvidas[i]['x'], result = table[i][QTD_COLUNAS]))
print('Z  =', z)