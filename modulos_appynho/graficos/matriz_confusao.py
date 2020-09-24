import matplotlib.pyplot as plt
import numpy as np

def matriz_confusao(lit_1,lit_2,padrao_usuario=False,salvar=False):

        padrao_local = {

            #=====================#
            # matriz | alterações referentes aos dados
            'residuo_geral':False,
            'tipo':'numerico',

            #=====================#
            # imagem | alterações referentes a imagem (todo)
            'salvar':False,
            'comprimento':6,
            'altura':5,
            'fonte':16,
            
            #=====================#
            # imagem | alterações referentes a imagem (local)
            'mapa_cor':plt.cm.Blues,
            'interpolacao':'nearest',
            'range':[0.0,1.0],
            'titulo':'',
            'legenda_1':False,
            'legenda_2':False,
            'cor':'w',
            'valor_1':'verdadeiro',
            'valor_2':'predito',
        }

        if padrao_usuario:
            
            for i in padrao_usuario:
                
                padrao_local[i] = padrao_usuario[i]

        # ::::::::::::::::::::::::::::::::::::::::::::::: #
        # Definição de variáveis

        s_1 = sorted(list(set(lit_1))) # lista dos elementos de lit_1
        s_2 = sorted(list(set(lit_2))) # lista dos elementos de lit_2

        n_valor = max([len(s_1),len(s_2)])

        # ::::::::::::::::::::::::::::::::::::::::::::::: #
        # salvando as labels (loop dos elementos)

        nms_1 = []
        for i in range(len(s_1)):
            if padrao_local['legenda_1']:
                nms_1.append(padrao_local['legenda_1'][int(s_1[i])])
            else:
                nms_1.append(int(s_1[i]))

        # ________________________ #

        nms_2 = []
        for i in range(len(s_2)):
            if padrao_local['legenda_1']:
                if padrao_local['legenda_2']:
                    nms_2.append(padrao_local['legenda_2'][int(s_2[i])])
                else:
                    nms_2.append(int(s_2[i]))
            else:
                nms_2.append(int(s_2[i]))

        # ::::::::::::::::::::::::::::::::::::::::::::::: #
        # Calculando o erro geral para apresentação

        err = []
        for i in range(len(lit_1)):
            if lit_1[i] == lit_2[i]:
                err.append(1)
            else:
                err.append(0)

        if padrao_local['residuo_geral']:
            print('acerto = ',sum(err),'de',len(err),'equivalente a',(sum(err)/len(err))*100.0,'%')

        # ::::::::::::::::::::::::::::::::::::::::::::::: #
        # calculo dos valores (por dicionário)

        CM = {}
        M2 = np.array([[0.0]*n_valor]*n_valor)
        M1 = []
        for j in range(len(s_1)):
            CM[int(s_1[j])] = {}
            M0 = []
            for i in range(len(s_2)):
                values = []
                for jj in range(len(lit_1)):
                    if lit_1[jj] == int(s_1[j]):
                        if lit_2[jj] == int(s_2[i]):
                            values.append(1)
                        else:
                            values.append(0)

                sv = sum(values)
                CM[int(s_1[j])][s_2[i]] = sv
                M2[j,i] = sv
                M0.append(sv)
            M1.append(M0)

        # ::::::::::::::::::::::::::::::::::::::::::::::: #
        # calculando proporções

        tamanho = len(lit_1)

        M1 = np.array(M1)

        if padrao_local['tipo'] == "numerico": # numeros de elementos contados (padrão)
            MF = M2.copy()

        # ________________________ #

        if padrao_local['tipo'] == "proporcao":

            MF = np.round((M2.astype('float') / M2.sum(axis=1)[:, np.newaxis]),3)
            onde_e_nan = np.isnan(MF)
            MF[onde_e_nan] = 0.000

        # ::::::::::::::::::::::::::::::::::::::::::::::: #
        # Tabela e gráficos
        
        fig = plt.figure(figsize=(padrao_local['comprimento'],padrao_local['altura']),dpi=200)
        im = plt.imshow(MF, interpolation=padrao_local['interpolacao'], cmap=padrao_local['mapa_cor'],vmin=padrao_local['range'][0], vmax=padrao_local['range'][1])
        plt.title(padrao_local['titulo'])
        cb = plt.colorbar(shrink=0.9145, fraction=0.1, pad=0.01)
        tick_marks_1 = np.arange(len(s_1))
        tick_marks_2 = np.arange(len(s_2))
        plt.xticks(tick_marks_1, nms_1, rotation=45,fontsize=padrao_local['fonte'])
        plt.yticks(tick_marks_2, nms_2,fontsize=padrao_local['fonte'])
        plt.ylabel(padrao_local['valor_2'],fontsize=padrao_local['fonte'])
        plt.xlabel(padrao_local['valor_1'],fontsize=padrao_local['fonte'])

        for i in range(MF.shape[0]):
            for j in range(MF.shape[1]):
                if type(padrao_local['cor']) == type('w'):
                    cor = padrao_local['cor']
                if type(padrao_local['cor']) == type({}):
                    for k in padrao_local['cor']:
                        if MF[i, j] >= padrao_local['cor'][k][0] and MF[i, j] < padrao_local['cor'][k][1]:
                            cor = k
                plt.text(j, i, MF[i, j],ha="center", va="center", color=cor, fontdict= {'fontsize':padrao_local['fonte']})

        
        if salvar:
            plt.savefig(salvar, bbox_inches="tight" )
        else:
            plt.show()