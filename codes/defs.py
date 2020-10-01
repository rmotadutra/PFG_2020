#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import numpy as np


def read_litho_types(path):
    """Reads the contents of a CSV file.

    Parameters
    ----------
    path : string
        The path of the file to read.

    Returns
    -------
    dict
        A dictionary containing the sections of the CSV file.
        
    Notes
    -----
    The CSV file should not have blank spaces, all lines of the file must have the same length.
    The structure of the returned dictionary is a dictionary inside other dictionary and is specified below.
    The first dictionary keys are the lithology names.
    The second dictionary keys are the others sections of the CSV file: 'COLOR', 'CODE'.
    
    Examples
    --------
    
    The examples below contains ficticious data.
    
    LITHOLOGY,COLOR,CODE
    SANDSTONE,#ffff3f,49
    SLURY,#7eff00,25
    SHALE,#006400,57
    SILTITE,#af1d4e,54
 
    The example below contain how to import the CSV file above, and what it returns.
    
    >>> import defs
    >>> csvfile = defs.read_litho_types('path/to/the/csv/file')
    >>> csvfile
    {'SANDSTONE': {'COLOR': '#ffff3f', 'CODE': '49'},
     'SLURY': {'COLOR': '#7eff00', 'CODE': '25'},
     'SHALE': {'COLOR': '#006400', 'CODE': '57'},
     'SILTITE': {'COLOR': '#af1d4e', 'CODE': '54'}}
    
    """
    import csv
    with open(path, errors="ignore") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        
        linhas = []
        for row in readCSV:
            linhas.append(row)
            
        data = {}
        for j in range(len(linhas[0])):
            lithology = []
            for i in range(1, len(linhas)):
                if j == 0:
                    data[linhas[i][j]] = {}
                else:
                    data[linhas[i][0]][linhas[0][j]] = linhas[i][j]    
            
    return data


def read_well(path, logs):
    """Reads the contents of a LAS 2.0 file.

    Parameters
    ----------
    path: string
        The path of the file to read.
        
    logs: list
        The names of the curves to be imported.

    Returns
    -------
    dict
        A dictionary containing the sections of the LAS file.

    Notes
    -----
    The structure of the returned dictionary is specified below.
    The dictionary keys are the curves names, that was reported in logs: 'DEPTH', 'GR', 'NPHI', 'RHOB'.
    Not all curves of the LAS file necessarily will be present on the dictionary.

    The value of each curve section is a numpy ndarray where contains the data from a well log.

    Examples
    --------
    
    The examples below contains ficticious data.
    The example below contain how to import a LAS file, and what returns.
    
    >>> import defs
    >>> lasfile = defs.read_well('path/to/the/las/file', ['DEPTH', 'GR', 'NPHI', 'RHOB'])
    >>> lasfile
    {'DEPTH': array([-4.5720000e-01, -3.0480000e-01, -1.5240000e-01, ...,
             3.5643312e+03,  3.5644836e+03,  3.5646360e+03]),
     'GR': array([  5.0502,   4.1305,   3.8073, ..., 125.6342, 125.6342, 125.6342]),
     'NPHI': array([-0.0517, -0.0541, -0.0101, ...,     nan,     nan,     nan]),
     'RHOB': array([nan, nan, nan, ..., nan, nan, nan])}
    
    """
    
    import las2 as las
    data = las.read(path)

    curves = {}
    for log in logs:
        for i, curve in enumerate(data['curve']):
            if curve['mnemonic'] == log:
                curves[log] = data['data'][i]
                
    return curves

def drdn (rhob, nphi):
    """Calculate DRDN curve.

    Parameters
    ----------
    rhob : numpy ndarray
        Data from RHOB curve.
        
    nphi : numpy ndarray
        Data from NPHI curve.

    Returns
    -------
    numpy ndarray
        A numpy ndarray containing the data of the DRDN curve.
    
    Examples
    --------
    
    The examples below contains ficticious data.
    
    >>> import defs
    >>> drdn = defs.drdn(RHOB, NPHI)
    >>> drdn
    array([nan, 5.3107, 4.7127, ..., 4.4874, 4.2507, nan])
    
    """
    drdn = ((rhob-2)/0.05) - ((0.45 - nphi)/0.03)

    return drdn

def create_lithology(drdn):
    
    lit_py = np.full(len(drdn), np.nan)

    # using the DRDN curve to interpret lithology 
    for i in range(len(drdn)):
        if drdn[i] < -1.0000:
            lit_py[i] = 49.000
        
        elif drdn[i] >= -1.0000 and drdn[i] < -0.3000 :
            lit_py[i] = 25.000
        
        elif drdn[i] >= -0.3000 and drdn[i] < 0.3000 :
            lit_py[i] = 54.000
        
        elif drdn[i] >= 0.3000:
            lit_py[i] = 57.000

    return lit_py

def separate_lithology(data, litho_types, curves):
    """Create separate well logs for each lithology.

    Parameters
    ----------
    data: dict
        The data that contains informations about the logs.
        
    litho_types: dict
        A dict that contains all the lithologies present in the well and its codes and colors.

    Returns
    -------
    dict
        An updated dictionary containing curves for each lithologies.

    Notes
    -----
    All input data is preserved, and the dict updated with logs from each lithology (GR, RHOB, NPHI) 

    The value of each curve section is a numpy ndarray that contains the data from a well log.

    Examples
    --------
    
    The examples below contains ficticious data.
    
    >>> import defs
    >>> separate_well = defs.separate_lithology(data, litho_types, ['LITHOLOGY', 'GR', 'RHOB', 'NPHI'])
    >>> separate_well
    {'DEPTH': array([-4.5720000e-01, -3.0480000e-01, -1.5240000e-01, ...,
             3.5643312e+03,  3.5644836e+03,  3.5646360e+03]),
     'GR': array([  5.0502,   4.1305,   3.8073, ..., 125.6342, 125.6342, 125.6342]),
     'NPHI': array([-0.0517, -0.0541, -0.0101, ...,     nan,     nan,     nan]),
     'RHOB': array([nan, nan, nan, ..., nan, nan, nan]),
     'DRDN': array([nan, nan, nan, ..., nan, nan, nan]),
     'LITHOLOGY': array([nan, nan, nan, ..., nan, nan, nan]),
     'SANDSTONE': {'LITHOLOGY': array([nan, nan, nan, ..., nan, nan, nan]),
      'GR': array([nan, nan, nan, ..., nan, nan, nan]),
      'NPHI': array([nan, nan, nan, ..., nan, nan, nan]),
      'RHOB': array([nan, nan, nan, ..., nan, nan, nan])},
     'SLURY': {'LITHOLOGY': array([nan, nan, nan, ..., nan, nan, nan]),
      'GR': array([nan, nan, nan, ..., nan, nan, nan]),
      'NPHI': array([nan, nan, nan, ..., nan, nan, nan]),
      'RHOB': array([nan, nan, nan, ..., nan, nan, nan])},
     'SHALE': {'LITHOLOGY': array([nan, nan, nan, ..., nan, nan, nan]),
      'GR': array([nan, nan, nan, ..., nan, nan, nan]),
      'NPHI': array([nan, nan, nan, ..., nan, nan, nan]),
      'RHOB': array([nan, nan, nan, ..., nan, nan, nan])},
     'SILTITE': {'LITHOLOGY': array([nan, nan, nan, ..., nan, nan, nan]),
      'GR': array([nan, nan, nan, ..., nan, nan, nan]),
      'NPHI': array([nan, nan, nan, ..., nan, nan, nan]),
      'RHOB': array([nan, nan, nan, ..., nan, nan, nan])}}
    
    """
    well = data   
    for lith in litho_types:
        well[lith] = {}
        w = data['LITHOLOGY'] == int(litho_types[lith]['CODE'])
        for curve in curves:
            well[lith][curve] = np.full(len(data['LITHOLOGY']), np.nan)
            well[lith][curve][w] = data[curve][w]
    
    return well


def formation_zone(data, top, base, curve=False):
    """Set a new top and base for the curves selected.

    Parameters
    ----------
    data : dict
        The data of the well.
        
    top : integer or float
        The new top depth.
    
    base: integer or float
        The new base depth.
        
    curve: list
        List with all curves that will be set a new top and base.

    Returns
    -------
    dict
        A dictionary containing the new data range of the selected curves.
        
    Notes
    -----
    
    If "curves" are not given, all the keys from "data" will be set in a new top and base.
    
    Examples
    --------
    
    The example below contains ficticious data.
    
    >>> import defs
    >>> zone = defs.formation_zone(data, 300.0, 2600.0, ['DEPTH', 'RHOB', 'NPHI'])
    >>> zone
    {'DEPTH': array([300.122 , 300.2744, 300.4268, ..., 2500.6636, 2500.816 ,
            2600.0]),
    'RHOB': array([2.6524, 2.6342, 2.6136, ..., 2.4002, 2.4042, 2.4056]),
    'NPHI': array([0.1985, 0.2366, 0.2627, ..., 0.3183, 0.2826, 0.2691])}
    
    """
    
    if curve:
        curve = curve
    else:
        curve = list(data.keys())
        
    w = (data['DEPTH'] >= top) & (data['DEPTH'] < base)
        
    formation = {}
    for log in curve:
        formation[log] = data[log][w]
    
    return formation

def statistic_lithology(data, lithology, curves, step, top=False, bottom=False, overlap=False):
    """Calculates the statistics for each lithology and for each curve.

    Parameters
    ----------
    data : dict
        The data of the well.
        
    lithology: list
        List with all lithologies that will calculate the statistics.
        
    curve: list
        List with all curves that will calculate the statistics.
        
    step: integer or float
        The value that the ranges will be divided.
        
    top : integer or float
        In what depth start the statistics.
    
    base: integer or float
        In what depth stop the statistics.

    Returns
    -------
    dict
        A dictionary containing the new statistics data of the selected curves and the selected lithologies.
        
    Notes
    -----
    
    It's possible to give the "curve" list and the "lithology" list in any order.
    
    If "top" and "base" are not given, the range of all well will be set to calculate the statistics.
    
    Examples
    --------
    
    The example below contains ficticious data.
    
    >>> import defs
    >>> statistics = defs.statistics_lithology(data, ['SANDSTONE'], ['GR'], 50.0, 2500, 3100)
    >>> zone
    {'DEPTH': array([2500.122 , 2500.2744, 2500.4268, ..., 3099.6636, 3099.816 ,
            3100.0]),
    'RHOB': array([2.6524, 2.6342, 2.6136, ..., 2.4002, 2.4042, 2.4056]),
    'NPHI': array([0.1985, 0.2366, 0.2627, ..., 0.3183, 0.2826, 0.2691]),
    'SANDSTONE': 'GR': {'Mean': {'2500.0-2550.0': nan,
                            '2550.0-2600.0': 37.74879393939394,
                            '2600.0-2650.0': 38.3727392,
                            '2650.0-2700.0': 38.270216201117314,
                            '2700.0-2750.0': 38.322155092592595,
                            '2750.0-2800.0': 40.29478794326241,
                            '2800.0-2850.0': 45.15985242290749,
                            '2850.0-2900.0': 46.77599699812383,
                            '2900.0-2950.0': 48.24150915697675,
                            '2950.0-3000.0': 48.62925721703012,
                            '3000.0-3050.0': 48.217977280858676,
                            '3050.0-3100.0': 48.217977280858676}
                          }
    }
    
    """
    if top:
        top = top
    else:
        top = min(data['DEPTH'])

    if bottom:
        bottom = bottom
    else:
        bottom = max(data['DEPTH'])

    if overlap:
        overlap = overlap
    else:
        overlap = 0.0

    tops = []
    bases = []
    base = top+step
    while base <= bottom:
        tops.append(top)
        bases.append(base)
        top = top + step - step*overlap
        base = base + step - step*overlap
    
    for lith in lithology:
        for curve in curves:
            curve_save = np.array(data[lith][curve])
            data[lith][curve] = {}
            data[lith][curve]['Data'] = curve_save
            data[lith][curve]['Mean'] = {}
            data[lith][curve]['Std'] = {}
            for t, b in zip(tops, bases):
                w = (data['DEPTH'] >= t) & (data['DEPTH'] <= b)
                mean = np.nanmean(curve_save[w])
                std = np.nanstd(curve_save[w])
                data[lith][curve]['Mean'][str(t) + '-' + str(b)] = mean
                data[lith][curve]['Std'][str(t) + '-' + str(b)] = std
                
    return data

def sort_curve(data, statistic, litho_types, curve, step, top=False, bottom=False, overlap=False):
    
    if top:
        top = top
    else:
        top = min(data['DEPTH'])

    if bottom:
        bottom = bottom
    else:
        bottom = max(data['DEPTH'])
        
    if overlap:
        overlap = overlap
    else:
        overlap = 0.0
    
    tops = []
    bases = []
    base = top+step
    while base <= bottom:
        tops.append(top)
        bases.append(base)
        top = top + step - step*overlap
        base = base + step - step*overlap
        
    value = np.full(len(data['LITHOLOGY']), np.nan)
    for i, (t, b) in enumerate(zip(tops, bases)):
        for lith in litho_types:
            w = (data['DEPTH'] >= t) & (data['DEPTH'] <= b) & (data['LITHOLOGY'] == int(litho_types[lith]['CODE']))
            mean = np.full(len(data['LITHOLOGY']), np.nan)
            mean[w] = list(statistic[lith][curve]['Mean'].values())[i]
            std = np.full(len(data['LITHOLOGY']), np.nan)
            std[w] = list(statistic[lith][curve]['Std'].values())[i]
            while np.isnan(mean[w].any()):
                i = i-1
                mean[w] = list(statistic[lith][curve]['Mean'].values())[i]
                std[w] = list(statistic[lith][curve]['Std'].values())[i]
            value[w] = np.random.normal(mean[w], std[w])
            
    return value


def corrcoef(steps, curve, depth):
    passos = steps

    coeficientes_correlação = []
    intervalo_profundidade = []

    for passo in range(passos): # 'passo' vai de 0 a 300

        # ------------------------------------------ #

        valor_h = [] # h  de head ou cabeça
        valor_t = [] # t de tail ou cauda

        for i in range(len(curve)-passo): # range menor que o passo para evitar o acesso em indices mais altos e não existentes
            valor_t.append(curve[i+passo])
            valor_h.append(curve[i])

        coeficientes_correlação.append(np.corrcoef(valor_h,valor_t)[1][0])
        intervalo_profundidade.append(depth[0+passo] - depth[0])

    # ------------------------------------------ #
    
    return intervalo_profundidade, coeficientes_correlação