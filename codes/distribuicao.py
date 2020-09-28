import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------- #

def local_litholigic_data(lithology,litho_info):
    
    lithos_index = {}
    
    m = len(lithology)
    for j in litho_info:
        index = []
        for i in range(m):
            if int(lithology[i]) == j:
                index.append(i)
        lithos_index[j] = index
        
    return lithos_index


def funcao_distribuicao(log,log_info,lito,lito_info,
                        normalization = False,graph=False,x_scale = False,y_scale = False,
                        salvar=False,legenda=False):
    
    # ................................................ #
    
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    
    self_MY = 0
    self_lithos_colors = []
    self_lithos_names  = []
    self_lithos_index  = []
    
    for i in lito_info:
        self_MY = self_MY + 1
        self_lithos_colors.append(lito_info[i][0])
        self_lithos_names.append(lito_info[i][1])
        self_lithos_index.append(lito[i])
    
    self_MX = 0
    self_max = []
    self_min = []
    self_data_names = []
    self_MEGA_DATA = []
    
    for i in log_info:
        self_MX = self_MX  + 1
        self_max.append(log_info[i][2][1])
        self_min.append(log_info[i][2][0])
        self_data_names.append(log_info[i][0])
        self_MEGA_DATA.append(log[i])
        
    #print(self_MX)
    
    # ................................................ #

    def _norm_n(c,p): # incorporate self

        dif = self_max[p] - self_min[p]

        self_normalized_data_a = ((c - self_min[p])/dif)

        return self_normalized_data_a

    # ................................................ #

    def _norm_s(c,p): # incorporate self
        a = 0.04
        b = 100
        self_normalized_data_b = 1.0/(1.0+np.exp(-a*c + a*b) ) 

        return self_normalized_data_b

    # ................................................ #

    def _gaussian(value,mean,sigma):

        gf = (1.0)/(sigma*np.sqrt(2.0*np.pi))
        gb = (-0.5)*((value - mean)/sigma)**2.0
        g = gf*np.exp(gb)

        return g
        
    # ................................................ #

    self_data_litho_matrix = []
    gaussian_mean = []
    gaussian_std = []
    l = 0
    
    # ................................................ #
    
    if graph:
        fig = plt.figure(figsize=(16,16))
    
    for k in range(self_MY):

        array_of_curves = []

        m_m = [] # local mean
        s_s = [] # local gaussian
        
        for j in range(self_MX):

            dif = self_max[j] - self_min[j]

            curve = []
            for i in self_lithos_index[k]:
                data_point = self_MEGA_DATA[j][i]
                if normalization:
                    curve.append(_norm_n(data_point,j))
                else:
                    curve.append(data_point)

            m = np.mean(curve)
            s = np.std(curve)

            m_m.append(m)
            s_s.append(s)

            g_distri = []
            for i in curve:
                g_distri.append(_gaussian(i,m,s))

            # ................................................ #

            if graph:

                l = l + 1
                ax = plt.subplot(len(self_lithos_index),len(self_MEGA_DATA), l)
                ax.hist(curve,400,density=True,color=self_lithos_colors[k])
                
                ms = '$\overline{m}$ = '+'{:.2f}'.format(m)+'$ | \sigma $ = '+'{:.2f}'.format(s)
                
                plt.plot(curve,g_distri,'.b', label='Gaussian'+' '+ms) ### gaussian
                plt.legend(loc='upper left',facecolor = 'w')

                if l < len(self_MEGA_DATA) + 1:
                    plt.title(self_data_names[j],fontsize = 20)

                if l % (len(self_MEGA_DATA))-1 == 0:
                    plt.ylabel(self_lithos_names[k],fontsize = 20)
                    
                ax.annotate('('+alfabeto[l-1]+')', xy=(1, 0), xycoords='axes fraction',
                                fontsize = 20,horizontalalignment='right', verticalalignment='bottom')
                
                if x_scale:
                    plt.xlim(x_scale)
                if y_scale:
                    plt.ylim(y_scale)
                    
                ax.patch.set_alpha(0.3)

        gaussian_mean.append(m_m)
        gaussian_std.append(s_s)

            # ................................................ #
    
    if salvar:
        plt.savefig(salvar[0], transparent=True, dpi = salvar[1], bbox_inches="tight")
    else:
        if graph:
            plt.show()
        
    return [gaussian_mean,gaussian_std]