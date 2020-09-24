import matplotlib.pyplot as plt

def pizza(proporcoes, info, padrao_usuario = False):

    padrao_local = {
        "posicao":'%1.0f%%',
        "fonte":18,
        "fonte_cor":"k",
        "figura_tamanho":(6,6),
        "sombra":False,
        "angulo_inicial":90,
        "salvar":False,
        "legenda_posicao":"best",
        "rosquinha":False,
        "explosao":0,
    }

    if padrao_usuario: 
        for i in padrao_usuario:
            padrao_local[i] = padrao_usuario[i]

    novas_proporcoes = proporcoes.copy()
    
    valores = []
    cores = []
    nomes = []
    explosao = []
    for i in proporcoes:
        valores.append(proporcoes[i])
        cores.append(info[i][0])
        nomes.append(info[i][1])
        explosao.append(padrao_local["explosao"])
    
    fig1, ax1 = plt.subplots()
    fig1.set_size_inches(padrao_local["figura_tamanho"])

    patches, texts, autotext = ax1.pie(valores, colors=cores, shadow=padrao_local["sombra"], startangle=padrao_local["angulo_inicial"],explode = explosao,
                                       autopct=padrao_local["posicao"],textprops={'fontsize': padrao_local["fonte"],'color':padrao_local["fonte_cor"]},pctdistance=0.9)
    plt.legend(patches,nomes,loc=padrao_local["legenda_posicao"])

    if padrao_local["rosquinha"]:
        centre_circle = plt.Circle((0,0),padrao_local["rosquinha"],fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

    ax1.axis('equal')
    if padrao_local["salvar"]:
        plt.savefig(padrao_local["salvar"][0], transparent=True, dpi = padrao_local["salvar"][1], bbox_inches="tight")
    plt.show()