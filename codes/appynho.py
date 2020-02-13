# Imports

import numpy as np

# --------------------------------------------------------------------------- #

import matplotlib.pyplot as plt

# --------------------------------------------------------------------------- #

import pandas as pd

import las2

# --------------------------------------------------------------------------- #

class plotagem:
    
    def __init__(self, n, eixoy=True, comprimento=6, altura=5, dpi=70, titulo = '', titulo_fonte = 16,
                cor_fundo = 'white',transparencia_fundo = 0.5,
                cor_plot_fundo = 'white',transparencia_plot_fundo = 1.0):
        self.ax = [0]*n
        fig, (self.ax) = plt.subplots(1,n,sharey=eixoy,figsize=(comprimento, altura),
                                 dpi=dpi)
        fig.suptitle(titulo, fontsize=titulo_fonte)
        
        fig.patch.set_facecolor(cor_fundo)
        fig.patch.set_alpha(transparencia_fundo)
        
        self.cor_plot_fundo = cor_plot_fundo
        self.transparencia_plot_fundo = transparencia_plot_fundo
    
    def plot_s(self,indice,X,Y,
             cor='b',estilo_linha = '-',
             descricao_x = 'x',descricao_y = 'y',fonte_descricao = 16,
             titulo = 'titulo',fonte_titulo = 15
            ):
        
        """plot simples"""
        
        self.ax[indice].plot(X,Y,c = cor,ls = estilo_linha)
        self.ax[indice].grid()
        self.ax[indice].set_ylim(max(Y),min(Y))
        self.ax[indice].set_title(titulo, fontsize=fonte_titulo)
        if indice == 0:
            self.ax[indice].set_ylabel(descricao_y, fontsize=fonte_descricao)
        self.ax[indice].set_xlabel(descricao_x, fontsize=fonte_descricao)
        
        self.ax[indice].patch.set_facecolor(self.cor_plot_fundo)
        self.ax[indice].patch.set_alpha(self.transparencia_plot_fundo)
        
    def plot_m(self,indice,XX,Y,cores = False,estilo_linha = '-',
              descricao_x = 'x',descricao_y = 'y',fonte_descricao = 16,
              titulo = 'titulo',fonte_titulo = 15):
        
        """plot multiplo"""
        
        if cores:
            crs = cores.copy()
        else:
            crs = ['b']*len(XX)
        
        for i in range(len(XX)):
            self.ax[indice].plot(XX[i],Y,c = crs[i],ls = estilo_linha)
        
        if indice == 0:
            self.ax[indice].set_ylabel(descricao_y, fontsize=fonte_descricao)
        self.ax[indice].set_xlabel(descricao_x, fontsize=fonte_descricao)
        self.ax[indice].set_title(titulo, fontsize=fonte_titulo)
        self.ax[indice].set_xticklabels([])
        
        self.ax[indice].patch.set_facecolor(self.cor_plot_fundo)
        self.ax[indice].patch.set_alpha(self.transparencia_plot_fundo)
        
    def plot_l(self,indice,litologia,Y,relacao_cor,curva_limite,minimo = False,maximo = False,
              descricao_x = '',descricao_y = 'y',fonte_descricao = 16,
              titulo = 'titulo',fonte_titulo = 15):
        
        """plot litologia"""

        codigos = []
        for i in relacao_cor:
            codigos.append(i)
            
        if minimo:
            minimo = minimo
        else:
            minimo = min(curva_limite)
            
        if maximo:
            maximo = maximo
        else:
            maximo = max(curva_limite)
        
        num_cores = len(codigos)
        
        matriz_litologias = np.array([[minimo]*len(curva_limite)]*num_cores)
        
        for j in range(num_cores):
            for i in range(len(matriz_litologias[j])):
                if litologia[i] == codigos[j] and  ~np.isnan(curva_limite[i]):
                    matriz_litologias[j][i] = curva_limite[i]
                    
        # =============================== #
        
        for i in range(num_cores):
            self.ax[indice].plot(matriz_litologias[i],Y,c = relacao_cor[codigos[i]],lw = 0.1)
            self.ax[indice].fill_betweenx(Y, matriz_litologias[i], facecolor=relacao_cor[codigos[i]])
        self.ax[indice].set_ylim(max(Y),min(Y))
        self.ax[indice].set_xlim(minimo,maximo)
        if indice == 0:
            self.ax[indice].set_ylabel(descricao_y, fontsize=fonte_descricao)
        self.ax[indice].set_xlabel(descricao_x, fontsize=fonte_descricao)
        self.ax[indice].set_title(titulo, fontsize=fonte_titulo)
        
        self.ax[indice].patch.set_facecolor(self.cor_plot_fundo)
        self.ax[indice].patch.set_alpha(self.transparencia_plot_fundo)
    
    def mostrar(self):
        plt.show()
        
    def salvar(self,caminho):
        fig.savefig(caminho, transparent=True)
        
# --------------------------------------------------------------------------- #
# ###
# --------------------------------------------------------------------------- #

class gerenciamento():
    
    def __init__(self):
        
        self.projetos = {}
        
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
                            print(i,'apelidado de',j)
                            dado_final[j] = dado[i]

            return dado_final

        # ------------------------------------ #

        else:
            return dado
    
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
    
    # ============================================ #
    
    def cropar(profundidade,curvas,topo=0,base=20000,nulos=False):

        novas_curvas = []
        for j in range(len(curvas)):
            curva = []
            profundiade_cropada = []
            for i in range(len(profundidade)):
                if profundidade[i] >= topo and profundidade[i] < base:
                    curva.append(curvas[j][i])
                    profundiade_cropada.append(profundidade[i])
            novas_curvas.append(curva)

        novas_curvas_final = []
        novas_curvas_final.append(profundiade_cropada)
        for i in range(len(curvas)):
            novas_curvas_final.append(novas_curvas[i])

        return novas_curvas_final
    
    # ============================================ #
    
    def cropar_limpo(profundidade,curvas,topo=0,base=20000,nulos=False):

        #nulos_idx = [True]*len(profundidade)

        novas_curvas = []
        for j in range(len(curvas)):
            curva = []
            profundiade_cropada = []
            for i in range(len(profundidade)):
                if profundidade[i] >= topo and profundidade[i] < base:
                    curva.append(curvas[j][i])
                    profundiade_cropada.append(profundidade[i])
            novas_curvas.append(curva)

        novas_curvas_final = []
        novas_curvas_final.append(profundiade_cropada)
        for i in range(len(curvas)):
            novas_curvas_final.append(novas_curvas[i])

        a = np.array(novas_curvas_final).T

        b = a[~np.isnan(a).any(axis=1)]
        if nulos:
            b = b[~np.isin(b,nulos).any(axis=1)]

        return list(b.T)

    # ============================================ #