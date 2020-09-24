import yaml
import utm
import numpy as np

import plotly.offline as pyo
import plotly.graph_objs as go

class mapas():

    # =========================== #

    def __init__(self):

        self.camadas_dados = []
        self.campos = {}
        self.mapbox_access_token = 'pk.eyJ1IjoibWFyaW8tdWZmIiwiYSI6ImNqdWl3ZmFqNjA1MGY0M280OTdka3RsNGEifQ.hvLN_LDGfu5F_XAkhz0tZg'

    # =========================== #

    def load_shape(self,data):

        with open(data) as file:
            self.campos = yaml.load(file, Loader=yaml.FullLoader)
        return self.campos

    # =========================== #

    def load_utm_data(self,data,cor='black'):

        map_data = {}
        map_data['nome'] = []
        map_data['lat'] = []
        map_data['lon'] = []
        map_data['cor'] = []

        for i in data:
            map_data['nome'].append(i)
            mapbox_dados = utm.to_latlon(data[i][0],data[i][1],24,'L')
            map_data['lat'].append(mapbox_dados[0])
            map_data['lon'].append(mapbox_dados[1])
            map_data['cor'].append(cor)

        return map_data

    def plot_pins(self,data):

        self.camadas_dados.append(
            go.Scattermapbox(data)
        )

    # =========================== #

    def plot_shape(self,data):

        self.camadas_dados.append(
            go.Scattermapbox(data)
        )

    # =========================== #

    def plot_border(self,coordinates):

        self.coordinates = np.array(coordinates)

        for i in range(2):
            self.plot_shape(
                {
                'lat':[-90,90],
                'lon':[coordinates[i][0],coordinates[i][0]],
                'fill':'toself',
                'fillcolor':'black',
                }
            )

            #######################

            self.plot_shape(
                {
                'lat':[coordinates[i][1],coordinates[i][1]],
                'lon':[-90,90],
                'fill':'toself',
                'fillcolor':'black',
                }
            )            

    # =========================== #

    def grid(self,n=11,r=2):

        xa = [round(i,r) for i in np.linspace(self.coordinates[:,0][0],self.coordinates[:,0][1],n)][1:-1]
        xb = xa.copy()
        ya = [self.coordinates[:,1][0]]*n
        yb = [self.coordinates[:,1][1]]*n

        xc = [round(i,r) for i in np.linspace(self.coordinates[:,1][0],self.coordinates[:,1][1],n)][1:-1]
        xd = xc.copy()
        yc = [self.coordinates[:,0][0]]*n
        yd = [self.coordinates[:,0][1]]*n
        #print(xa,xb,ya,yb)

        for i in range(len(xa)):
            self.plot_shape(
                {
                'lon':[xa[i],xb[i]],
                'lat':[ya[i],yb[i]],
                'fill':'toself',
                'fillcolor':'rgba(220,220,220,1.0)',
                'marker':{'size':0}
                }
            )

            self.plot_pins(
            {
                'lon':[xa[i]],
                'lat':[yb[i]],
                'text':[str(xa[i])],
                'mode':'markers+text',
                'textposition':'bottom center',
                'textfont':{
                    'color':"grey",
                    'size':9
                },
                'marker':{
                    'size':0,
                }

            })

            #######################

            self.plot_shape(
                {
                'lat':[xc[i],xd[i]],
                'lon':[yc[i],yd[i]],
                'fill':'toself',
                'fillcolor':'rgba(220,220,220,1.0)',
                'marker':{'size':0}
                }
            )

            self.plot_pins(
            {
                'lat':[xc[i]],
                'lon':[yd[i]],
                'text':[str(xc[i])],
                'mode':'markers+text',
                'textposition':"middle left",
                'textfont':{
                    'color':"grey",
                    'size':9
                },
                'marker':{
                    'size':0,
                }

            })  

    # =========================== #

    def show(self,info):

        base_info = {
            'autosize':True,
            #'hovermode':['x unified'],
            'showlegend':False,
            'width':1000,
            'height':1000,
            'mapbox':{}
        }

        for i in info:
            base_info[i] = info[i]

        base_info['mapbox']['accesstoken'] = self.mapbox_access_token
        base_info['mapbox']['bearing'] = 0
        base_info['mapbox']['pitch'] = 0

    # =========================== #

        fig = go.Figure(data=self.camadas_dados, layout=base_info)
        pyo.iplot(fig, filename='Teste')