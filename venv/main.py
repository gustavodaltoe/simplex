import re


# INIT - FUNÇOES DE ABERTURA E FECHAMENTO DE ARQUIVO
openFile = lambda name, mode: open(name, mode)
closeFile = lambda file: file.close()
# END - FUNÇOES DE ABERTURA E FECHAMENTO DE ARQUIVO

FILENAME = 'entrada.txt'

# INIT - COLETANDO LINHAS DA FILE
file = openFile(FILENAME, 'r')
fileLines = file.readlines()
closeFile(file)
# END - COLETANDO LINHAS DA FILE


#Z = AX + BY
# x = formatLines(fileLines[0])

print(fileLines[1])


