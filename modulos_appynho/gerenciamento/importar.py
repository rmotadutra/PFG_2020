import pandas as pd
import numpy as np
import platform
import os # importar_pasta

from . import las2

class acesso():
    
    def __init__(self):
        
        self.projetos = {}
        
    # ============================================ #
    
    def acesso(dicionario):
        
        if platform.system() == "Windows":
            return dicionario['WIN']
        else:
            return dicionario['LINUX']
        
        
    def importar_pasta(caminho_geral,ext = '.las'):

        #------------------------------------------------------------------#
        # vai conter o caminho até os arquivos em geral
        arquivos = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(caminho_geral):
            for file in f:
                if ext in file:
                    arquivos.append(os.path.join(r, file))

        #------------------------------------------------------------------#
        # arquivos = caminho geral ate os arquivos
        # names = nomes dos poços

        if platform.system() == "Linux":
            c_resumo = caminho_geral+'/'
        if platform.system() == "Windows":
            c_resumo = caminho_geral+'\\'

        dado = {}
        for i in arquivos:
            n1 = i.replace(c_resumo, '')
            dado[n1.replace(ext,'')] = i

        return dado
        
    # ============================================ #
    
    def importar_las(caminho,apelidos=False):

        campo = {}

        dado_lido = las2.read(caminho)

        nomes = [a['mnemonic'] for a in dado_lido['curve']]
        unidades = [a['unit'] for a in dado_lido['curve']]
        dado = {}
        for i in range(len(nomes)):
            dado[nomes[i]] = dado_lido['data'][i]

        # ------------------------------------ #

        if apelidos:
            dado_final = {}
            for i in dado:
                for j in apelidos:
                    for k in apelidos[j]:

                        if i == k:
                            #print(i,'apelidado de',j)
                            dado_final[j] = dado[i]

            return dado_final

        # ------------------------------------ #

        else:
            return dado
    
    # ============================================ #
    
    def poco_info(arquivo,apelidos):
    
        poco = las2.read(arquivo)

        coordenadas = {}

        for k in apelidos:
            for j in apelidos[k]:
                for i in poco['well']:
                    if i['mnemonic'] == j:
                        coordenadas[k] = i['value']

        return coordenadas
    
    # ============================================ #    
        
    def importar_csv(caminho,profundidades,mnemonico):

        dado = pd.read_csv(caminho)

        print("cabecalho =",dado.columns.values)

        dado_final = {}

        for i in list(dado.columns.values):
            for j in mnemonico:
                for k in mnemonico[j]:

                    if i == k:
                        print(i,'apelidado de',j)
                        dado_final[j] = list(dado[i])

        lito = dado_final['codigo']
        ptop = dado_final['topo']
        pbot = dado_final['base']

        lito_2 = [0.0]*len(profundidades)

        for j in range(len(ptop)):
            for i in range(len(profundidades)):
                if profundidades[i] >= ptop[j] and profundidades[i] < pbot[j]:
                    lito_2[i] = lito[j]

        return lito_2
    
    # ============================================ #
    
    def importar_dados(caminhos,pocos=False):
            
        # ------------------------------------ #
            
        campo = {}
        for j in range(len(caminhos)):

            dado_lido = las2.read(caminhos[j])

            nomes = [a['mnemonic'] for a in dado_lido['curve']]
            unidades = [a['unit'] for a in dado_lido['curve']]
            dado = {}
            for i in range(len(nomes)):
                dado[nomes[i]] = dado_lido['data'][i]

            campo[caminhos[j]] = [dado,nomes,unidades]
            
        return [nomes,campo]