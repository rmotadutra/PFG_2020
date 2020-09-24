import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def analise_dispersao(logs,logs_info,lito_log,lito_log_info,padrao_usuario = False):
    
    # =============================== #
    
    padrao_programa = {
        
        # tudo o que pode ser alterado
        'resolucao':72,
        'titulo':'',
        'titulo_fonte':16,
        'posicao':False,
        'salvar':False,
        'legenda':False,
        'histograma_diverso':{'alpha':0.4,'bins':30},
        'figura_tamanho':(16,16),
    }
    
    if padrao_usuario:
        
        for i in padrao_usuario:
            
            padrao_programa[i] = padrao_usuario[i]

    if padrao_programa['histograma_diverso'] == False:
        alfa = 0.4
    else:
        alfa = padrao_programa['histograma_diverso']['alpha']
            
    # =============================== #        
    
    MX = len(logs_info)
    
    local_data_names = []
    local_data = []
    
    for i in logs_info:
        local_data_names.append(logs_info[i][0])
        local_data.append(logs[i])
    
    # =============================== #
    
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    
    local_lithos_colors = []
    local_lithos_index = []
    MY = len(lito_log_info)
    
    for i in lito_log_info:
        local_lithos_colors.append(lito_log_info[i][0])
        
    for j in lito_log_info:
        mini_index = []
        for i in range(len(lito_log)):
            if lito_log[i] == j:
                mini_index.append(i)
        local_lithos_index.append(mini_index)
    
    # =============================== #
    # separacao litologias
    
    if padrao_programa['histograma_diverso']:
        all_data = []
        for k in logs_info: # por curva
            mini_data = []
            for j in lito_log_info: # por cor
                curve = []
                for i in range(len(lito_log)): # por profundidade
                    if lito_log[i] == j:
                        curve.append(logs[k][i])
                mini_data.append(curve)
            all_data.append(mini_data)
    
    # =============================== #
    # legendas
    
    if padrao_programa['legenda']:
        
        std_legenda = {
            'posicao':(-1.7,1.0,2.0,-3.5),
            'fonte':16,
            'transparencia':0.9,
            'colunas':4,
            'modo':"expand",
            'borda':0.0
        }
    
    # =============================== #
        
        for i in padrao_programa['legenda']:
            
            std_legenda[i] = padrao_programa['legenda'][i]
        
        lab = []
        for i in lito_log_info:
                lab = lab + [mpatches.Patch(label=lito_log_info[i][1],color=lito_log_info[i][0])]
    
    # =============================== #
    
    fig = plt.figure(figsize=padrao_programa['figura_tamanho'], dpi=padrao_programa['resolucao'])
    fig.suptitle(padrao_programa['titulo'], fontsize=padrao_programa['titulo_fonte'], y=0.91)
    # ----------------------------------------------------------- #

    l = 0
    for k1 in range(MX):
        for k2 in range(MX):
            l = l + 1

            if k1 == k2:
                ax = fig.add_subplot(MX,MX, l)
                if padrao_programa['histograma_diverso']:
                    for i in range(MY):
                        ax.hist(all_data[k1][i],padrao_programa['histograma_diverso']['bins'],color=local_lithos_colors[i],
                                alpha=alfa) ###
                else:
                    ax.hist(local_data[k1],100) ###
                
                
                ax.patch.set_alpha(0.0)
                if padrao_programa['posicao']:
                    ax.annotate('('+alfabeto[l-1]+')', xy=(posicao[0], posicao[1]), xycoords='axes fraction',
                                fontsize = posicao[4],horizontalalignment='right', verticalalignment='bottom')

            if k1 != k2:
                ax = fig.add_subplot(MX,MX, l)
                D1 = local_data[k1]
                D2 = local_data[k2]
                if padrao_programa['posicao']:
                     ax.annotate('('+alfabeto[l-1]+')', xy=(posicao[2], posicao[3]), xycoords='axes fraction',
                                fontsize = posicao[4],horizontalalignment='right', verticalalignment='bottom')


                for j in range(len(local_lithos_colors)):
                    gr = [];dt = []
                    for i in range(len(local_lithos_index[j])):
                        gr.append(D1[local_lithos_index[j][i]])
                        dt.append(D2[local_lithos_index[j][i]])
                    ax.plot(dt,gr,'.',alpha=alfa,color=local_lithos_colors[j])
                    ax.patch.set_alpha(0.0)

            if l < MX + 1:
                plt.title(local_data_names[k2],fontsize = padrao_programa['titulo_fonte'])

            if l % (MX)-1 == 0:
                plt.ylabel(local_data_names[k1],fontsize = padrao_programa['titulo_fonte'])
                
        if padrao_programa['legenda']:
            if k1 == 0:
                ax.legend(handles=lab, bbox_to_anchor=std_legenda['posicao'],
                          loc=0, ncol=std_legenda['colunas'], mode=std_legenda['modo'],
                          borderaxespad=std_legenda['borda'],
                          fontsize=std_legenda['fonte']).get_frame().set_alpha(std_legenda['transparencia'])
                
    if padrao_programa['salvar']:
        plt.savefig(padrao_programa['salvar'][0], transparent=True, dpi = padrao_programa['salvar'][1], bbox_inches="tight")
    else:
        plt.show()