import numpy as np

# ------------------------------------------------------------- #

def prop_test(curve):
    qt = sorted(list(set(curve)))
    
    summ = {}
    for j in qt:
        l_c = []
        for i in curve:
            if i == j:
                l_c.append(1)
        summ[j] = sum(l_c)/len(curve)
    
    return summ

# ------------------------------------------------------------- #

def per100(proporcao):
    nova_proporcao = {}
    for i in proporcao:
        nova_proporcao[i] = proporcao[i]*100
        
    return nova_proporcao

# ------------------------------------------------------------- #

def local_litholigic_data(lithology,litho_info):
    
    lithos_index = {}
    
    m = len(lithology) # MY
    for j in litho_info:
        index = []
        for i in range(m):
            if int(lithology[i]) == j:
                index.append(i)
        lithos_index[j] = index
        
    return lithos_index

# ------------------------------------------------------------- #

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
    
# ------------------------------------------------------------- #

def cropar_limpo(profundidade,curvas,topo=0,base=20000,nulos=False):

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

# ------------------------------------------------------------- #

def cropar_limpo_2(profundidade,curvas,topo=0,base=20000,nulos=False):

    p2 = []
    for j in curvas:
        curva = []
        for i in range(len(curvas[j])):
            if profundidade[i] >= topo and profundidade[i] < base:
                curva.append (curvas[j][i])

        p2.append(curva)

    a = np.array(p2).T
    b = a[~np.isnan(a).any(axis=1)]
    if nulos:
        b = b[~np.isin(b,nulos).any(axis=1)]

    c = b.T

    log_limpo = {}
    i = 0
    for key in curvas:
        log_limpo[key] = c[i]
        i += 1

    return log_limpo

# ------------------------------------------------------------- #

class correcao_profundidade():
    
    def __init__(self,prof,c):
        
        self.prof = prof
        self.c = c
        
        self.fatores = []
        self.reta = []
        
    # ================================== #
    
    def minimos_quadrados(self,prof,c):
        
        x = np.array(prof)
        y = np.array(c)
        o = np.array([1.0]*len(x))
        G = np.array([x,o])
        Gt = np.transpose(G)
        Gi = np.linalg.inv(np.dot(G,Gt))
        g1 = np.dot(Gt,Gi)
        self.fatores = np.dot(g1.T,y)
        self.reta = self.calcular_reta(x)

        return self.reta
    
    # ================================== #
    
    def calcular_reta(self,prof):
        
        nova_propriedade = []
        for i in range(len(prof)):
            nova_propriedade.append((prof[i]*self.fatores[0]) + self.fatores[1])
            
        return nova_propriedade
    
    # ================================== #
    
    def localizar_minimos(self):
        
        self.novo_c = []
        self.novo_prof = []
        for i in range(len(self.c)):
            if self.c[i] < self.reta[i]:
                self.novo_c.append(self.c[i])
                self.novo_prof.append(self.prof[i])
                
        return (self.novo_c,self.novo_prof)
                
    # ================================== #
                
    def reta_minima(self):
        
        rm1 = self.minimos_quadrados(self.novo_prof,self.novo_c)
        rm2 = self.calcular_reta(self.prof)
        
        new_c = []
        for i in range(len(self.prof)):
            new_c.append(self.c[i] - rm2[i])
            
        return new_c
            
    # ================================== #
    
    def ajuste_simples(self):
        
        etapa1 = self.minimos_quadrados(self.prof,self.c)
        
    
    # ================================== #
    
    def ajuste_duplo(self):
        
        etapa1 = self.minimos_quadrados(self.prof,self.c)
        etapa2 = self.localizar_minimos()
        etapa3 = self.reta_minima()

        return etapa3
    
# ------------------------------------------------------------- #