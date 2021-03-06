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

# Quantidade de linhas e de colunas
qtd_linhas = int(input("Digite o número de linhas: "))
qtd_colunas = int(input("Digite o número de colunas: "))

def codePacket(originalPacket):
    ##
    # Argumentos:
    #  - originalPacket: pacote original a ser codificado na forma de uma lista.
    # Cada entrada na lista representa um bit do pacote (inteiro 0 ou 1).
    # Valor de retorno: pacote codificado no mesmo formato.
    ##

    # Tamnho do bloco sem codificação
    TAM_BLOCO = qtd_linhas * qtd_colunas

    # Quantidade de blocos de bits que serão codificados
    QTD_BLOCOS = len(originalPacket) // TAM_BLOCO

    # Tamanho total do bloco codificado = 32bits de dados(8*4) + 8bits paridade linha + 4bits paridade coluna
    TAM_BLOCO_COD = TAM_BLOCO + qtd_linhas + qtd_colunas

    # Tamanho do pacote após codificação, que será o produto da quantidade de blocos de 32bits do pacote original e o
    # tamanho do bloco após a codificação
    TAM_PACOTE_COD = QTD_BLOCOS * TAM_BLOCO_COD

    # Geração da matriz de paridade
    matriz_paridade = [[0 for c in range(qtd_colunas)] for l in range(qtd_linhas)]

    # Vetor que receberá os bits do pacote após a codificação
    pacote_codificado = [0] * TAM_PACOTE_COD

    # Iteração para a codificação dos blocos de 32 bits
    for bloco in range(QTD_BLOCOS):
        # Iteração das n linhas
        for linha in range(qtd_linhas):
            # Iteração das n colunas de uma linha
            for coluna in range(qtd_colunas):
                matriz_paridade[linha][coluna] = originalPacket[linha * (qtd_colunas - 1) + linha + coluna]

        # Replicação dos dados no pacote codificado
        for posicao in range(TAM_BLOCO):
            pacote_codificado[bloco * TAM_BLOCO_COD + posicao] = originalPacket[bloco * TAM_BLOCO + posicao]

        # Cálculo da paridade das colunas
        for coluna in range(qtd_colunas):
            paridade_coluna = 0
            for linha in range(qtd_linhas):
                paridade_coluna = paridade_coluna + matriz_paridade[linha][coluna]
            pacote_codificado[bloco * TAM_BLOCO_COD + TAM_BLOCO + coluna] = 0 if paridade_coluna % 2 == 0 else 1

        # Cálculo da paridade das linhas
        for linha in range(qtd_linhas):
            paridade_linha = 0
            for coluna in range(qtd_colunas):
                paridade_linha = paridade_linha + matriz_paridade[linha][coluna]
            pacote_codificado[
                bloco * TAM_BLOCO_COD + TAM_BLOCO + qtd_colunas + linha] = 0 if paridade_linha % 2 == 0 else 1

    return pacote_codificado


##
# Executa decodificacao do pacote transmittedPacket, gerando
# novo pacote decodedPacket.
##
def decodePacket(transmittedPacket):

    # Tamnho do bloco_cod sem codificação
    TAM_BLOCO = qtd_linhas * qtd_colunas

    # Quantidade de blocos de 32 bits que serão codificados
    QTD_BLOCOS = len(originalPacket) // TAM_BLOCO

    # Tamanho total do bloco_cod codificado = 32bits de dados(8*4) + 8bits paridade linha + 4bits paridade coluna
    TAM_BLOCO_COD = TAM_BLOCO + qtd_linhas + qtd_colunas

    # Tamanho do pacote após codificação, que será o produto da quantidade de blocos de 32bits do pacote original e o
    # tamanho do bloco_cod após a codificação
    TAM_PACOTE_COD = QTD_BLOCOS * TAM_BLOCO_COD

    # Geração da matriz de paridade
    matriz_paridade = [[0 for c in range(qtd_colunas)] for l in range(qtd_linhas)]

    paridade_coluna = [0 for c in range(qtd_colunas)]

    paridade_linha = [0 for c in range(qtd_linhas)]

    # Geração do vetor que armazena os bits decodificados
    pacote_decodificado = []

    # Itera por cada bloco_cod codificado
    for bloco_cod in range(0, TAM_PACOTE_COD, TAM_BLOCO_COD):

        # Bits de dados dos blocos são dispostos na matriz
        for linha in range(qtd_linhas):
            for coluna in range(qtd_colunas):
                matriz_paridade[linha][coluna] = transmittedPacket[linha * (qtd_colunas - 1) + linha + coluna]

        # Bits de paridade das colunas
        for coluna in range(qtd_colunas):
            paridade_coluna[coluna] = transmittedPacket[bloco_cod + TAM_BLOCO + coluna]

        # Bits de paridade das linhas
        for linha in range(qtd_linhas):
            paridade_linha[linha] = transmittedPacket[bloco_cod + TAM_BLOCO + qtd_colunas + linha]

        # Verificação das paridades das linhas
        linha_erro = None
        for linha in range(qtd_linhas):
            paridade = 0
            for coluna in range(qtd_colunas):
                paridade = paridade + matriz_paridade[linha][coluna]
            if paridade % 2 != paridade_linha[linha]:
                linha_erro = linha
                break

        # Verificação dos bits de paridade das colunas
        coluna_erro = None
        for coluna in range(qtd_colunas):
            paridade = 0
            for linha in range(qtd_linhas):
                paridade = paridade + matriz_paridade[linha][coluna]
            if paridade % 2 != paridade_coluna[coluna]:
                coluna_erro = coluna
                break

        if (linha_erro is not None) and (coluna_erro is not None):
            matriz_paridade[linha_erro][coluna_erro] = 1 if matriz_paridade[linha_erro][coluna_erro] == 0 else 1

        for linha in matriz_paridade:
            for b in linha:
                pacote_decodificado.append(b)

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
