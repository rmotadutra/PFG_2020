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
    The structure of the returned dictionary is a dictionary inside other dictionary and is specified below.
    
    The first dictionary keys are the lithology names.
    
    The second dictionary keys are the others sections of the CSV file: 'COLOR', 'CODE'.
    
    Examples
    --------
    
    """
    import csv
    with open(path, errors="ignore") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        linhas = []
        for row in readCSV:
            linhas.append(row)

        data = {}
        lithology = []
        color = []
        code = []
        for i in range(1, len(linhas)):
            lithology.append(linhas[i][0])
            color.append(linhas[i][1])
            code.append(linhas[i][2])

        ii=0
        for i in lithology:
            #print(i)
            data[i] = {}
            data[i][linhas[0][1]] = color[ii]
            data[i][linhas[0][2]] = code[ii]
            ii += 1
            
    return data


def read_well(well_path):
    """Reads the contents of a LAS 2.0 file.

    Parameters
    ----------
    well_path : string
        The path of the file to read.

    Returns
    -------
    dict
        A dictionary containing the sections of the LAS file.

    Notes
    -----
    The structure of the returned dictionary is specified below.
    The dictionary keys are the curves names: 'DEPTH', 'GR', 'NPHI', 'RHOB'.
    Not all curves be present on the dictionary.

    The value of each curve section is a numpy ndarray where contains the data from a well log.

    Examples
    --------
    """
    
    import las2 as las
    data = las.read(well_path)
    for i in range(len(data['curve'])):
        if data['curve'][i]['mnemonic'] == 'DEPTH':
            depth = data['data'][i]
        elif data['curve'][i]['mnemonic'] == 'GR':
            gr = data['data'][i]
        elif data['curve'][i]['mnemonic'] == 'NPHI':
            nphi = data['data'][i]
        elif data['curve'][i]['mnemonic'] == 'RHOB':
            rhob = data['data'][i]
            
    curves = {'Depth': depth,
              'GR': gr,
              'NPHI': nphi,
              'RHOB': rhob}
    return curves

def drdn (rhob, nphi):
    """Calculate DRDN curve.

    Parameters
    ----------
    rhob : numpy ndarray
        The data of the RHOB curve.
        
    nphi : numpy ndarray
        The data of the NPHI curve.

    Returns
    -------
    drdn
        A numpy ndarray containing the data of the DRDN curve.
    
    Examples
    --------
    
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

def separate_lithology (data, litho_types):
    lito_code = []
    for lito in set(data['LITHOLOGY']):
        lito_code.append(lito)
    lito_code = np.array(lito_code)
    lito_code = lito_code[~np.isnan(lito_code)]
    lito_code = sorted(lito_code)
    
    lito_all = []
    gr_all = []
    nphi_all = []
    rhob_all = []
    for i in range(len(lito_code)):
        lito1 = []
        gr_lito = []
        nphi_lito = []
        rhob_lito = []
        for j in range(len(data['Depth'])):
            if data['LITHOLOGY'][j] == lito_code[i]:
                value = data['LITHOLOGY'][j]
                gr = data['GR'][j]
                nphi = data['NPHI'][j]
                rhob = data['RHOB'][j]
            else:
                value = np.nan
                gr = np.nan
                nphi = np.nan
                rhob = np.nan
            lito1.append(value)
            gr_lito.append(gr)
            nphi_lito.append(nphi)
            rhob_lito.append(rhob)
        lito_all.append(lito1)
        gr_all.append(gr_lito)
        nphi_all.append(nphi_lito)
        rhob_all.append(rhob_lito)
    
    litho ={}
    k = 0
    for i in lito_code:
        for j in litho_types:
            if int(litho_types[j]['CODE']) == int(i):
                litho[j] = {}
                litho[j]['LITHOLOGY'] = np.array(lito_all[k])
                litho[j]['GR'] = np.array(gr_all[k])
                litho[j]['NPHI'] = np.array(nphi_all[k])
                litho[j]['RHOB'] = np.array(rhob_all[k])
                k += 1
    
    return litho