import random
import math
import sys

#########
# Implementacao um esquema sem qualquer metodo de codificao.
#
# Cada byte do pacote original eh mapeado para o mesmo byte no pacote
# codificado.
########

###
##
# Funcoes a serem alteradas!
##
###

##
# Codifica o pacote de entrada, gerando um pacote
# de saida com bits redundantes.
##
qtd_linhas = int(input("Digite o número de linhas para a matriz de paridade: "))
qtd_colunas = int(input("Digite o número de colunas para a matriz de paridade: "))


def codePacket(originalPacket):

    # Matriz que será usada para calcular as paridades bidimensionais
    matriz_paridade = [[0 for _ in range(qtd_colunas)] for __ in range(qtd_linhas)]
    pacote_codificado = []

    # Tamanho do bloco de bits utilizados para o calculo de paridade bidimensional
    tam_bloco = qtd_linhas * qtd_colunas
    tam_pacote = len(originalPacket)

    # Quantidade de blocos necessários para o calculo de paridade bidimensional
    qtd_blocos = (tam_pacote // tam_bloco)
    bits_restantes = 0
    # Caso o tamanho do pacote não seja um múltiplo do tamanho do bloco,
    # será necessário um bloco a mais para calcular a paridade de todos os bits
    if (tam_pacote % tam_bloco != 0) and (tam_pacote > tam_bloco):
        qtd_blocos = qtd_blocos + 1

    for bloco in range(qtd_blocos):

        # preencher a matriz de paridade com os bits relativos ao bloco
        for linha in range(qtd_linhas):
            for coluna in range(qtd_colunas):
                matriz_paridade[linha][coluna] = originalPacket[(bloco * tam_bloco) + linha * qtd_colunas + coluna]

        # preencher o pacote codificado com os bits relativos ao bloco
        for b in range(tam_bloco):
            pacote_codificado.append(originalPacket[(bloco * tam_bloco) + b])

        # calcular as paridades das colunas e inseri-las no pacote codificado
        for coluna in range(qtd_colunas):
            paridade = 0
            for linha in range(qtd_linhas):
                paridade = paridade + matriz_paridade[linha][coluna]

            # Trabalhando com paridade par
            if paridade % 2 == 0:
                pacote_codificado.append(0)
            else:
                pacote_codificado.append(1)

        # calcular as paridades das linhas e inseri-las no pacote codificado
        for linha in range(qtd_linhas):
            paridade = 0
            for coluna in range(qtd_colunas):
                paridade = paridade + matriz_paridade[linha][coluna]

            # trabalhando com paridade par
            if paridade % 2 == 0:
                pacote_codificado.append(0)
            else:
                pacote_codificado.append(1)

    return pacote_codificado


##
# Executa decodificacao do pacote transmittedPacket, gerando
# novo pacote decodedPacket.
##
def decodePacket(transmittedPacket):

    # Matriz que será usada para calcular as paridades bidimensionais
    matriz_paridade = [[0 for _ in range(qtd_colunas)] for __ in range(qtd_linhas)]
    paridade_linha = [0 for _ in range(qtd_linhas)]
    paridade_coluna = [0 for _ in range(qtd_colunas)]
    pacote_decodificado = []

    # Tamanho do bloco
    tam_bloco = qtd_linhas * qtd_colunas

    # Tamanho do bloco codificado
    tam_bloco_cod = tam_bloco + (qtd_linhas + qtd_colunas)

    # Tamnho do pacote codificado
    tam_pacote_cod = len(transmittedPacket)

    for bloco in range(0, tam_pacote_cod, tam_bloco_cod):

        # Preencher a matriz paridade com os bits relativos ao bloco
        for linha in range(qtd_linhas):
            for coluna in range(qtd_colunas):
                matriz_paridade[linha][coluna] = transmittedPacket[bloco + linha * qtd_colunas + coluna]

        # preencher o vetor paridade_coluna
        for coluna in range(qtd_colunas):
            paridade_coluna[coluna] = transmittedPacket[bloco + tam_bloco + coluna]

        # preencher o vetor paridade_linha
        for linha in range(qtd_linhas):
            paridade_linha[linha] = transmittedPacket[bloco + tam_bloco + qtd_colunas + linha]

        # verificar paridade das colunas
        coluna_erro = None
        for coluna in range(qtd_colunas):
            paridade = 0
            for linha in range(qtd_linhas):
                paridade = paridade + matriz_paridade[linha][coluna]
            paridade = paridade % 2
            if paridade != paridade_coluna[coluna]:
                coluna_erro = coluna
                break

        # verificar paridade das linhas
        linha_erro = None
        for linha in range(qtd_linhas):
            paridade = 0
            for coluna in range(qtd_colunas):
                paridade = paridade + matriz_paridade[linha][coluna]
            paridade = paridade % 2
            if paridade != paridade_linha[linha]:
                linha_erro = linha
                break

        # Correção de erros
        if (linha_erro is not None) and (coluna_erro is not None):
            if matriz_paridade[linha_erro][coluna_erro] == 0:
                matriz_paridade[linha_erro][coluna_erro] = 1
            else:
                matriz_paridade[linha_erro][coluna_erro] = 0

        # Preenchimento do pacote decodificado
        for linha in range(qtd_linhas):
            for coluna in range(qtd_colunas):
                pacote_decodificado.append(matriz_paridade[linha][coluna])

    return pacote_decodificado


###
##
# Outras funcoes.
##
###

##
# Gera conteudo aleatorio no pacote passado como
# parametro. Pacote eh representado por um vetor
# em que cada posicao representa um bit.
# Comprimento do pacote (em bytes) deve ser
# especificado.
##
def generateRandomPacket(l):
    return [random.randint(0, 1) for x in range(8 * l)]


##
# Gera um numero pseudo-aleatorio com distribuicao geometrica.
##
def geomRand(p):
    uRand = 0
    while (uRand == 0):
        uRand = random.uniform(0, 1)

    return int(math.log(uRand) / math.log(1 - p))


##
# Insere erros aleatorios no pacote, gerando uma nova versao.
# Cada bit tem seu erro alterado com probabilidade errorProb,
# e de forma independente dos demais bits.
# Retorna o numero de erros inseridos no pacote e o pacote com erros.
##
def insertErrors(codedPacket, errorProb):
    i = -1
    n = 0  # Numero de erros inseridos no pacote.

    ##
    # Copia o conteudo do pacote codificado para o novo pacote.
    ##
    transmittedPacket = list(codedPacket)

    while 1:

        ##
        # Sorteia a proxima posicao em que um erro sera inserido.
        ##
        r = geomRand(errorProb)
        i = i + 1 + r

        if i >= len(transmittedPacket):
            break

        ##
        # Altera o valor do bit.
        ##
        if transmittedPacket[i] == 1:
            transmittedPacket[i] = 0
        else:
            transmittedPacket[i] = 1

        n = n + 1

    return n, transmittedPacket


##
# Conta o numero de bits errados no pacote
# decodificado usando como referencia
# o pacote original. O parametro packetLength especifica o
# tamanho dos dois pacotes em bytes.
##
def countErrors(originalPacket, decodedPacket):
    errors = 0

    for i in range(len(originalPacket)):
        if originalPacket[i] != decodedPacket[i]:
            errors = errors + 1

    return errors


##
# Exibe modo de uso e aborta execucao.
##
def help(selfName):
    sys.stderr.write("Simulador de metodos de FEC/codificacao.\n\n")
    sys.stderr.write("Modo de uso:\n\n")
    sys.stderr.write("\t" + selfName + " <tam_pacote> <reps> <prob. erro>\n\n")
    sys.stderr.write("Onde:\n")
    sys.stderr.write("\t- <tam_pacote>: tamanho do pacote usado nas simulacoes (em bytes).\n")
    sys.stderr.write("\t- <reps>: numero de repeticoes da simulacao.\n")
    sys.stderr.write("\t- <prob. erro>: probabilidade de erro de bits (i.e., probabilidade\n")
    sys.stderr.write("de que um dado bit tenha seu valor alterado pelo canal.)\n\n")

    sys.exit(1)


##
# Programa principal:
#  - le parametros de entrada;
#  - gera pacote aleatorio;
#  - gera bits de redundancia do pacote
#  - executa o numero pedido de simulacoes:
#      + Introduz erro
#  - imprime estatisticas.
##

##
# Inicializacao de contadores.
##
totalBitErrorCount = 0
totalPacketErrorCount = 0
totalInsertedErrorCount = 0

##
# Leitura dos argumentos de linha de comando.
##
if len(sys.argv) != 4:
    help(sys.argv[0])

packetLength = int(sys.argv[1])
reps = int(sys.argv[2])
errorProb = float(sys.argv[3])

if packetLength <= 0 or reps <= 0 or errorProb < 0 or errorProb > 1:
    help(sys.argv[0])

##
# Inicializacao da semente do gerador de numeros
# pseudo-aleatorios.
##
random.seed()

##
# Geracao do pacote original aleatorio.
##

originalPacket = generateRandomPacket(packetLength)
codedPacket = codePacket(originalPacket)

##
# Loop de repeticoes da simulacao.
##
for i in range(reps):

    ##
    # Gerar nova versao do pacote com erros aleatorios.
    ##
    insertedErrorCount, transmittedPacket = insertErrors(codedPacket, errorProb)
    totalInsertedErrorCount = totalInsertedErrorCount + insertedErrorCount

    ##
    # Gerar versao decodificada do pacote.
    ##
    decodedPacket = decodePacket(transmittedPacket)

    ##
    # Contar erros.
    ##
    bitErrorCount = countErrors(originalPacket, decodedPacket)

    if bitErrorCount > 0:
        totalBitErrorCount = totalBitErrorCount + bitErrorCount
        totalPacketErrorCount = totalPacketErrorCount + 1

print('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
print('Numero de bits transmitidos: {0:d}'.format(reps * packetLength * 8))
print('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
print('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(
    float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
print('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
print('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(
    float(totalBitErrorCount) / float(reps * packetLength * 8) * 100.0))
print('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
print('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))


