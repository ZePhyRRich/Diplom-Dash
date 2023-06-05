import base64
import datetime
import io
import os

import dash
from dash import Dash, html, dcc, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import urllib.parse


import plotly.express as px
import pandas as pd
import numpy as np


dash.register_page(__name__, path_template="/load/<name>", name='WHAT') # '/' is home page
current_directory = os.getcwd()
files = os.listdir(f"{current_directory}\library")

print("Текущая директория:", f"{current_directory}\library")

def layout(name=None):
    
    if name == None:
        return dbc.Container([
            html.H1('Пусто тут')
        ])
    decoded_param = urllib.parse.unquote(name)
    print(decoded_param)
    df = pd.read_excel(f"{current_directory}\library\{decoded_param}")
    print(df)
    print(len(df.axes[1]))
    if len(df.axes[1])==3:
        tab1 = dbc.Tab([dcc.Graph(figure=px.bar(df, x=df.columns[0], y=[df.columns[1], df.columns[2]], barmode='group'))], label="Столбчатая диаграмма",id="tab_1")
        tab2 = dbc.Tab([dcc.Graph(figure=px.histogram(df, x=df.columns[0], y=[df.columns[1], df.columns[2]], barmode='group'))], label="Гистограмма")
        tab3 = dbc.Tab([
            dcc.Graph(figure=px.pie(df, values=df.columns[1], names=df.columns[0])),
            dcc.Graph(figure=px.pie(df, values=df.columns[2], names=df.columns[0])),
        ], label="Круговая диаграмма")
        statistics1 = df[df.columns[1]].describe()
        data1 = {
            'Статистика': ['Среднее значение', 'Стандартное отклонение', 'Минимальное значение', 'Максимальное значение'],
            'Значение': [statistics1['mean'], statistics1['std'], statistics1['min'], statistics1['max']]
        }
        statistics2 = df[df.columns[2]].describe()
        data2 = {
            'Статистика': ['Среднее значение', 'Стандартное отклонение', 'Минимальное значение', 'Максимальное значение'],
            'Значение': [statistics2['mean'], statistics2['std'], statistics2['min'], statistics2['max']]
        }
        df_stat1 = pd.DataFrame(data1)
        df_stat2 = pd.DataFrame(data2)

        df_table = dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.Br(),
                                html.H5(f"{df.columns[1]}",style={'fontSize':24, 'textAlign':'center'}),
                                html.Hr(),
                                dbc.Table.from_dataframe(
                                        df_stat1,
                                        id='table-loads-out',
                                    
                                        ),
                            ])
                            
                        ]),
                        dbc.Col([
                            dbc.Card([
                                html.Br(),
                                html.H5(f"{df.columns[2]}",style={'fontSize':24, 'textAlign':'center'}),
                                html.Hr(),
                                dbc.Table.from_dataframe(
                                        df_stat2,
                                        id='table-loads-out2',
                                    
                                        ),
                            ])
                            
                        ])
                        

                       
                    ])    

    else:
        tab1 = dbc.Tab([dcc.Graph(figure=px.bar(df, x=df.columns[0], y=df.columns[1], color=df.columns[0]))], label="Столбчатая диаграмма",id="tab_1")
        tab2 = dbc.Tab([dcc.Graph(figure=px.histogram(df, x=df.columns[0], y=df.columns[1], color=df.columns[0]))], label="Гистограмма")
        tab3 = dbc.Tab([dcc.Graph(figure=px.pie(df, values=df.columns[1], names=df.columns[0]))], label="Круговая диаграмма")
        statistics1 = df[df.columns[1]].describe()
        data1 = {
            'Статистика': ['Среднее значение', 'Стандартное отклонение', 'Минимальное значение', 'Максимальное значение'],
            'Значение': [statistics1['mean'], statistics1['std'], statistics1['min'], statistics1['max']]
        }
        df_stat1 = pd.DataFrame(data1)  
        df_table = html.Div([
                        html.Br(),
                        html.H5(f"{df.columns[1]}",style={'fontSize':24, 'textAlign':'center'}),
                        html.Hr(),
                        dbc.Table.from_dataframe(
                        df_stat1,
                        id='table-loads-out',
                    
                        )
                    ])    
    tab4 = dbc.Tab([
        dbc.Table.from_dataframe(
            df,
            id='table-loads-out',
           
            )
    ], label="Таблица")
    
    
    
    
    return dbc.Container([
        html.Div(f'{decoded_param[:-5]}',
                         style={'fontSize':34, 'textAlign':'center'}),
        dbc.Card(dbc.Tabs([tab1, tab2, tab3, tab4],active_tab="tab_load_1")),
        df_table
       
    ])
   
