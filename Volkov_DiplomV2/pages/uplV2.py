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

dash.register_page(__name__, path='/excel_view', name='Загрузка') # '/' is home page

layout = dbc.Container(
    [
        html.H1("Загрузка файла: "),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Перетащите файл сюда, или ',
                html.A('Выберите его')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        
            multiple=True,
            # style = {
            #     'width': '75%',
            # }
    ),

    # dcc.Dropdown(
    #     file_options
    # , id='file-browser'),
    html.Div([
        html.Div(id='output-div'),
        html.Div(id='output-datatable'),
    ])
    
    
    ]
)

# OPTION_FIG = {
#     'Круговая':'Круговая',
#     'Гистограмма':'Гистограмма',
#     'Столбчатая':'Столбчатая',

# }

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Если загрузили CSV
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            df = df.dropna()
        elif 'xls' in filename:
            # Если загрузили Эксель
            df = pd.read_excel(io.BytesIO(decoded))
            df = df.dropna()
    except Exception as e:
        print(e)
        return html.Div([
            'Ошибка, не подходящий файл!'
        ])

    return html.Div([

        html.Hr(),
        html.Div([
            html.H5('Общие сведения:',style={'textAlign':'center'}),
            html.H5(filename, id='filename'),
            html.H6(datetime.datetime.fromtimestamp(date)),
        ]),
        html.Hr(),


        html.H5('Надстройки',style={'textAlign':'center'}),
        
        dbc.Row([

            dbc.Col([
                html.H5("Ось Х"),
                dcc.Dropdown(id='xaxis-data',
                            options=[{'label':x, 'value':x} for x in df.columns],
                            value=df.columns[0]),
                html.H5("Отбор"),
                dcc.Dropdown(
                        id="x-input",
                        options= [],
                        multi=True,
                        placeholder="Выберите ОО"),
            ]),

            dbc.Col([
                html.H5("Ось Y"),
                dcc.Dropdown(id='yaxis-data',
                            options=[{'label':x, 'value':x} for x in df.columns]),
                html.H5("Доп Y"),
                dcc.Dropdown(id='y-input',
                            options=[{'label':x, 'value':x} for x in df.columns]),
            ])

        ]),

              

        html.H5('Таблица',style={'textAlign':'center'}),
        dash_table.DataTable(
            data=df.to_dict('records'),
            id='table_out',
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=10,
            # editable=True,
            # cell_selectable=True,
            # filter_action="native",
            # sort_action="native",
            style_table={"overflowX": "auto"},
            # row_selectable="multi",
            style_cell={
            'textAlign': 'center'  # Выравнивание по центру ячейки
            },
        ),

        html.Hr(),

        html.Div(
            id='stat-div'
        ),
  
        
        dcc.Store(id='stored-data', data=df.to_dict('records')),

        html.Hr(),  

        
        



        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])


@callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@callback(Output('output-div', 'children'),
            #   Input('submit-button','n_clicks'),
            Input('table_out','data'),
            Input('xaxis-data','value'),
            Input('yaxis-data', 'value'),
            Input('x-input', 'value'),
            State('y-input', 'value'),
           )
def make_graphs(data, x_data, y_data, x_input, y_input):
    if (data is None) or (x_data is None) or (y_data is None):
        return dash.no_update
    df=pd.DataFrame(data)
    dff = df[df[x_data].isin(x_input)] 
    print(dff)
    if y_input:
        tab1 = dbc.Tab([dcc.Graph(figure=px.bar(dff, x=x_data, y=[y_data, y_input], barmode='group'))], label="Столбчатая диаграмма",id="tab_1")
        tab2 = dbc.Tab([dcc.Graph(figure=px.histogram(dff, x=x_data, y=[y_data, y_input], barmode='group'))], label="Гистограмма")
        tab3 = dbc.Tab([
            dcc.Graph(figure=px.pie(dff, values=y_data, names=x_data)),
            dcc.Graph(figure=px.pie(dff, values=y_input, names=x_data)),
        ], label="Круговая диаграмма")
    else:
        tab1 = dbc.Tab([dcc.Graph(figure=px.bar(dff, x=x_data, y=y_data, color=x_data))], label="Столбчатая диаграмма",id="tab_1")
        tab2 = dbc.Tab([dcc.Graph(figure=px.histogram(dff, x=x_data, y=y_data, color=x_data))], label="Гистограмма")
        tab3 = dbc.Tab([dcc.Graph(figure=px.pie(dff, values=y_data, names=x_data))], label="Круговая диаграмма")
        
    # tab4 = dbc.Tab([
    #     dash_table.DataTable(
    #         data=dff.to_dict('records'),
    #         id='table_out',
    #         columns=[{'name': i, 'id': i} for i in df.columns],
    #         page_size=10,
    #         # editable=True,
    #         # cell_selectable=True,
    #         # filter_action="native",
    #         # sort_action="native",
    #         style_table={"overflowX": "auto"},
    #         # row_selectable="multi",
    #         style_cell={
    #         'textAlign': 'center'  # Выравнивание по центру ячейки
    #         },)
    # ], label="Таблица")
    tab5 = dbc.Tab([
            dbc.InputGroup(
            [
                dbc.Button("Сохранить график", id="save-button", className="btn btn-success"),
                dbc.Input(id="filename-input", placeholder="Введите название"),
               
            ]
        ),
        # dcc.Input(id='filename-input',placeholder="Введите название"),
        # html.Button("Сохранить график", id="save-button")
    ],label="Настройки")
    # if choose_fig == 'Столбчатая':
    #     bar_fig = px.bar(data, x=x_data, y=y_data, color=x_data)
    #     # print(data)
    #     return dcc.Graph(figure=bar_fig)

    # if choose_fig == 'Гистограмма':
    #     bar_fig = px.histogram(data, x=x_data, y=y_data, color=x_data)
    #     # print(data)
    #     return dcc.Graph(figure=bar_fig)

    # if choose_fig == 'Круговая':
    #     bar_fig = px.pie(data, values=y_data, names=x_data)
    #     # print(data)
    #     return dcc.Graph(figure=bar_fig)
    return dbc.Card(dbc.Tabs([tab1, tab2, tab3, tab5],active_tab="tab_1"))


@callback(
    Output('stat-div', 'children'),
    Input('table_out','data'),
    Input('xaxis-data','value'),
    Input('yaxis-data','value'),
)
def make_graphs(table_data, x_data, y_data):
    sum = 0
    count = 0
    dff = pd.DataFrame.from_records(table_data)
    for i in dff[y_data]:
        sum=sum+i
        count = count + 1

    result_table = {
        'Сумма':sum,
        'Кол-во':count,
        'Среднее':sum/count,
    }

    rt = pd.DataFrame(data=result_table, index=[x_data])
    print(f'''
        Сумма = {sum}
        Кол-во = {count}
        Среднее = {sum/count}
    ''')

    children = html.Div([
        html.P(f"Статистические данные по столбцу '{y_data}'"),
        dash_table.DataTable(
            id='res-table',
            data = rt.to_dict('records'),
            style_table={'overflowX': 'auto'},
            page_size=10,
        ),

    ])
    return children

# Вывод 2-х столбцов
@callback(
            Output('table_out', 'data'),
            Input('xaxis-data','value'),
            Input('yaxis-data', 'value'),
            Input('x-input', 'value'),
            Input('y-input', 'value'),
            State('stored-data','data'),
            )
def update_data_table(x_data, y_data, x_input, y_input, data):
    if (x_data is None) or (y_data is None):
        return dash.no_update
    if y_input:
        columns_to_keep = [x_data, y_data, y_input]
    else:
        columns_to_keep = [x_data, y_data]
    new_df = pd.DataFrame.from_records(data)
    new_df = new_df.loc[:, columns_to_keep]
    new_df = new_df[new_df[x_data].isin(x_input)] 
    return new_df.to_dict('records')

@callback(
            Output('table_out', 'columns'),

            Input('table_out', 'data'),
    )
    
def update_columns_table(data):

    df = pd.DataFrame(data)
    updated_columns = [{'name': col, 'id': col} for col in df.columns]
    
    return updated_columns


@callback(
    Output('filename-input', 'value'),
    Input('save-button', 'n_clicks'),
    State('filename-input', 'value'),
    State('table_out','data'),
    State('filename','children'),
    State('xaxis-data','value'),
    State('yaxis-data', 'value'),
    State('x-input', 'value'),
    State('y-input', 'value'),
    prevent_initial_call=True,
)
def save_table_to_excel(n_clicks, filename, data, old_filename,x_data,y_data,x_input,y_input):
    df = pd.DataFrame(data)
    print(old_filename)
    print(filename)
    # Создаем Excel файл с использованием имени, введенного в текстовое поле
    if filename is None:
        if x_input and y_input:
            df.to_excel(f'library/{old_filename[:-5]}_X={x_input}_Y={y_data}_Y2={y_input}.xlsx', index=False)
        if (x_input is None) and y_input:
            df.to_excel(f'library/{old_filename[:-5]}_X={x_data}_Y={y_data}_Y2={y_input}.xlsx', index=False)
        if (x_input) and (y_input is None):
            df.to_excel(f'library/{old_filename[:-5]}_X={x_input}_Y={y_data}.xlsx', index=False)
        if (x_input is None) and (y_input is None):
            df.to_excel(f'library/{old_filename[:-5]}_X={x_data}_Y={y_data}.xlsx', index=False)
    else:
        df.to_excel(f'library/{filename}.xlsx', index=False)

    return ''

#Опции для Отбора"
@callback(
    Output('x-input', 'options'),
    Input('xaxis-data', 'value'),
    State('stored-data', 'data'),
)
def setOptionsTOO(x_data, data):
    df = pd.DataFrame(data)
    return [{'label':x, 'value':x} for x in df[x_data].unique()]

#Значения для "Отбора"
@callback(
    Output('x-input', 'value'),
    Input('x-input', 'options'),
)
def setValuesTOO(value_options):
    return [x['value'] for x in value_options]


# Вывод 2-х столбцов
# @callback(Output('table_out', 'columns'),
#               Input('reload-button','n_clicks'),
#               State('stored-data','data'),
#               State('xaxis-data','value'),
#               State('yaxis-data', 'value'),
#               State('choose-fig', 'value'),)
# def make_graphs(n, data, x_data, y_data, choose_fig):
#     if n is None:
#         return dash.no_update
#     columns= [{'name': col, 'id': col} for col in [x_data, y_data]]
#     return columns