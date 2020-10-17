import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

with open('noFECcopyp5.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    tamanho_pacote=[]
    Numero_transmitidos=[]
    Numero_errados_inseridos=[]
    Numero_corrompidos_apos_decodificacao=[]
    for row in reader:
         
         tamanho_pacote.append(row['Tamanho do pacote'])
         Numero_transmitidos.append(row['Numero de bits transmitidos'])
         Numero_errados_inseridos.append(row['Numero de bits errados inseridos'])
         Numero_corrompidos_apos_decodificacao.append(row['Numero de bits corrompidos apos decodificacao'])
         
tamanho_pacote = list(map(int, tamanho_pacote)) # converte a lista de strings em lista de números float

Numero_transmitidos = list(map(int, Numero_transmitidos))
Numero_errados_inseridos = list(map(int, Numero_errados_inseridos))
Numero_corrompidos_apos_decodificacao = list(map(int, Numero_corrompidos_apos_decodificacao))



print(tamanho_pacote)
print(Numero_transmitidos)
print(Numero_errados_inseridos)
print(Numero_corrompidos_apos_decodificacao)

#{'Número de linhas':qtd_linhas,'Número de colunas':qtd_colunas,'Tamanho do pacote': (qtd_linhas*qtd_colunas) ,'Numero de transmissoes simuladas': reps,'Numero de bits transmitidos': (reps * packetLength * 8),'Numero de bits errados inseridos':totalInsertedErrorCount,'Taxa de erro de bits (antes da decodificacao)': '{0:.2f}%'.format(float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0),'Numero de bits corrompidos apos decodificacao': totalBitErrorCount ,'Taxa de erro de bits (apos decodificacao)':'{0:.2f}%'.format((float(totalBitErrorCount) / float(reps * packetLength * 8) * 100.0)),'Numero de pacotes corrompidos':totalPacketErrorCount,'Taxa de erro de pacotes':'{0:.2f}%'.format((float(totalPacketErrorCount) / float(reps) * 100.0)) }) 

x = np.arange(len(tamanho_pacote))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, Numero_errados_inseridos, width, label='Numero de bits errados inseridos',color ='r')
rects2 = ax.bar(x + width/2, Numero_corrompidos_apos_decodificacao, width, label='Numero de bits corrompidos apos decodificacao',color ='b')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Numero de bits errados inseridos')
ax.set_xlabel('Tamanho do Pacote em bits')
ax.set_title('Matriz de Paridade Bidimensional \n Relação da Quantidade de erros inseridos e número de bits corrompidos apos decodificacao pelo tamanho do pacote')
ax.set_xticks(x)
ax.set_xticklabels(tamanho_pacote)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.show()