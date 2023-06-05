import base64
import datetime
import io
import os

import dash
from dash import Dash, html, dcc, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc


import plotly.express as px
import pandas as pd
import numpy as np


dash.register_page(__name__, path='/load', name='Открыть') # '/' is home page





link_style = {
    'text-decoration': 'none',
}

layout = dbc.Container(
    children=[
        html.H1('Список файлов'),
        
        html.Div(
            id = 'div-out'
        ),


        dcc.Interval(
            interval=5*1000, # in milliseconds
            n_intervals=0,
            id='interval'
        )



       

                # html.Thead(
                #     html.Tr(
                #         children=[
                #             html.Th('Имя файла')
                #         ]
                #     )
                # ),
                # html.Tbody(
                #     [
                #         html.Tr(
                #             children=[
                #                 html.Td(
                #                     html.A(f'Открыть файл {file}', id='open-link', href=f'load\{file}')
                #                 )

                #             ]
                #         )
                #         for file in files
                #     ]
                # )
            # html.Table(
            # style=table_style,
            # children=[]
        # ),
        # html.Div(id="page_content"),

    ]
)


@callback(
    Output('div-out','children'),
    Input('interval','n_intervals')
)
def live_update(intervals):
    current_directory = os.getcwd()
    files = os.listdir(f"{current_directory}\library")
    children = [
        dbc.Alert(
                    children=[html.A(
                        children=[
                            html.Div(
                                children=f"{file}",
                                id='plaque'
                            )
                        ],
                        id='open-link', 
                        href=f'load\{file}',
                        style=link_style,
                        className="alert-link"
                    )],
                    color="primary",
                    
                ) for file in files
    ]
    return children

# @callback(
#     Output('plaque', 'style'),
#     Input('plaque', 'n_mouseover'),
#     Input('plaque', 'n_mouseout'),
#     State('plaque', 'style')
# )
# def update_plaque_style(n_mouseover, n_mouseout, style):
#     if n_mouseover is None and n_mouseout is None:
#         return style
#     else:
#         new_style = style.copy()
#         new_style['background-color'] = '#ff5722' if n_mouseover else '#f44336'
#         return new_style

# # Обработчик события изменения URL-адреса
# @callback(Output('page-content', 'children'),
#             Input('open-link', 'href'))
# def display_page(pathname):
#     df = pd.read_excel(files + '\\' + pathname[1:])  # Удаляем ведущий слэш из pathname
#     print(pathname)
#     print(df)
#     return  dash_table.DataTable(
#             data=df.to_dict('records'),
#             id='table_load_out',
#             columns=[{'name': i, 'id': i} for i in df.columns],
#             page_size=10,
#             # editable=True,
#             # cell_selectable=True,
#             # filter_action="native",
#             # sort_action="native",
#             style_table={"overflowX": "auto"},
#             # row_selectable="multi",
#             style_cell={
#             'textAlign': 'center'  # Выравнивание по центру ячейки
#             },)
