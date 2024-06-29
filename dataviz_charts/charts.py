import pandas as pd
from pandas import DataFrame
import re
import pandas as pd
import plotly.graph_objects as go
from typing import List
import plotly.express as px
pd.set_option('display.max_columns', None)
pd.set_option('display.max_seq_items', None)


def extract_text_between_quotes(string):
    pattern = r"'(.*?)'"
    matches = re.findall(pattern, string)
    return matches

def clean_education_level(text: str) -> str:
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('Ã§', 'ç')
    text = text.replace('Ã£', 'ã')
    text = text.replace('Ã³', 'ó')
    text = text.replace('Ã', 'ã')
    text = text.strip()
    return text

def substituir_nivel_ensino(nivel: str) -> str:
    mapeamento_nivel_ensino = {
    'PÃ³s-graduaÃ§Ã£o': 'Pós-graduacao',
    'GraduaÃ§Ã£o/Bacharelado': 'Graduacao/Bacharelado',
    'Doutorado ou Phd': 'Doutorado ou Phd',
    'Estudante de GraduaÃ§Ã£o': 'Estudante de Graduação',
    'Mestrado': 'Mestrado',
    'NÃ£o tenho graduaÃ§Ã£o formal': 'Nao tenho graduacao formal',
    'Prefiro nÃ£o informar': 'Prefiro nao informar'
}
    return mapeamento_nivel_ensino.get(nivel, nivel)

def clean_salary_range(salary: str) -> str:
    return salary.replace('mÃªs', 'mês')

def clean_data(df: DataFrame) -> DataFrame:
    df.columns = [extract_text_between_quotes(column_name)[1] if len(extract_text_between_quotes(column_name)) > 1 else column_name for column_name in list(df.columns)]

    df = df[df['Genero'] != 'Prefiro não informar']
    df = df[df['Genero'] != 'Outro']
    df['Nivel de Ensino'] = df['Nivel de Ensino'].apply(substituir_nivel_ensino)
    df['Faixa salarial'] = df['Faixa salarial'].apply(lambda x: clean_salary_range(x) if pd.notna(x) else x)

    return df


def plot_age_distribution_by_gender(df: DataFrame) -> None:
    """
    Plota a distribuição de idade por gênero a partir de um arquivo CSV.

    :param path: Caminho para o arquivo CSV.
    :param encoding: Codificação do arquivo CSV.
    """
    print(f'colunas {df.columns}')

    data_filtered = df.dropna(subset=['Idade', 'Faixa idade', 'Genero'])

    data_aggregated = data_filtered.groupby(['Faixa idade', 'Genero']).size().reset_index(name='count')

    fig = go.Figure()

    color_dict = {
    'Masculino': '#0A77BE', 
    'Feminino': '#FF008E',
    }
    for gender in data_aggregated['Genero'].unique():
        df_gender = data_aggregated[data_aggregated['Genero'] == gender]
        fig.add_trace(go.Bar(
            x=df_gender['Faixa idade'],
            y=df_gender['count'],
            name=gender,
            marker_color=color_dict[gender]
        ))

    fig.update_layout(
        title='Distribuição de Idade por Gênero',
        xaxis_title='Faixa de Idade',
        yaxis_title='Contagem',
        barmode='group'
    )

    return fig


def plot_age_distribution_with_proportions_by_gender(df: pd.DataFrame) -> None:
    """
    Plota a distribuição de idade por gênero a partir de um DataFrame, mostrando proporções.

    :param df: DataFrame contendo os dados.
    """
    data_filtered = df.dropna(subset=['Idade', 'Faixa idade', 'Genero'])
    total_por_genero = data_filtered.groupby('Genero').size()
    #fazendo proporção
    data_aggregated = data_filtered.groupby(['Faixa idade', 'Genero']).size().reset_index(name='count')
    data_aggregated['percentage'] = data_aggregated.apply(lambda row: (row['count'] / total_por_genero[row['Genero']]) * 100, axis=1)

    fig = go.Figure()

    color_dict = {
    'Masculino': '#0A77BE', 
    'Feminino': '#FF008E',
    }

    for gender in data_aggregated['Genero'].unique():
        df_gender = data_aggregated[data_aggregated['Genero'] == gender]
        fig.add_trace(go.Bar(
            x=df_gender['Faixa idade'],
            y=df_gender['percentage'],
            name=gender,
            marker_color=color_dict[gender]
        ))

    fig.update_layout(
        title='Distribuição de Idade por Gênero (Normalizado)',
        xaxis_title='Faixa de Idade',
        yaxis_title='Porcentagem',
        barmode='group',
        font=dict(
            family='Arial',
            size=12 
        )
    )
    return fig


def plot_age_distribution_pie_chart(df: DataFrame, genero: str) -> None:
    """
    Plota um gráfico de pizza para a distribuição de faixas de idade de um determinado gênero a partir de um DataFrame.

    :param df: DataFrame contendo os dados.
    :param genero: Gênero para o qual o gráfico de pizza será gerado.
    """

    data_filtered = df[df['Genero'] == genero].dropna(subset=['Idade', 'Faixa idade', 'Genero'])

    faixa_etaria_order = ['17-21', '22-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54']
    data_filtered['Faixa idade'] = pd.Categorical(data_filtered['Faixa idade'], categories=faixa_etaria_order, ordered=True)

    data_aggregated = data_filtered.groupby('Faixa idade').size().reset_index(name='count')

    colors_dict = {
        '17-21': '#25384B',
        '22-24': '#799951',
        '25-29': '#0A77BE',
        '30-34': '#FF008E', 
        '35-39': '#c2c2f0',
        '40-44': '#ffb3e6',
        '45-49': '#c2f0c2',
        '50-54': '#ff6666',
    }

    colors = [colors_dict[faixa] for faixa in data_aggregated['Faixa idade']]

    fig = go.Figure(data=[go.Pie(
        labels=data_aggregated['Faixa idade'],
        values=data_aggregated['count'],
        texttemplate='<b>%{label}</b><br>%{percent}',
        textinfo='percent+label',
        pull=[0.1 for _ in range(len(data_aggregated))],
        hole=0.4,
        sort=False,
        marker=dict(colors=colors)
    )])

    fig.update_layout(
        title=f'Distribuição de Faixa de Idade para {genero}',
    )
    fig.update_traces(rotation=40)
    return fig


def plot_stacked_bar_percentage_education_level_by_gender(df: DataFrame) -> None:
    """
    Plota um gráfico de barras empilhadas para Nível de Ensino por Gênero a partir de um DataFrame, mostrando porcentagens.

    :param df: DataFrame contendo os dados.
    """
    data_filtered = df.dropna(subset=['Genero', 'Nivel de Ensino'])

    total_por_genero = data_filtered.groupby('Genero').size()

    data_aggregated = data_filtered.groupby(['Nivel de Ensino', 'Genero']).size().reset_index(name='count')
    data_aggregated['percentage'] = data_aggregated.apply(lambda row: (row['count'] / total_por_genero[row['Genero']]) * 100, axis=1)
    order_list = ['Prefiro não informar','Não tenho graduação formal','Estudante de Graduação','Graduação/Bacharelado','Pós-graduação','Mestrado','Doutorado ou Phd']
    data_aggregated['Nivel de Ensino'] = pd.Categorical(data_aggregated['Nivel de Ensino'], categories=order_list, ordered=True)
    data_aggregated = data_aggregated.sort_values(by=['Nivel de Ensino'])
    fig = go.Figure()

    color_dict = {
    'Masculino': '#0A77BE', 
    'Feminino': '#FF008E',
    }

    for gender in data_aggregated['Genero'].unique():
        df_gender = data_aggregated[data_aggregated['Genero'] == gender]
        fig.add_trace(go.Bar(
            x=df_gender['Nivel de Ensino'],
            y=df_gender['percentage'],
            name=gender,
            marker_color=color_dict[gender] 
        ))

    fig.update_layout(
        title='Nível de Ensino por Gênero (Normalizado)',
        xaxis_title='Nível de Ensino',
        yaxis_title='Porcentagem',
        barmode='stack'
    )
    return fig


def plot_mapa(df, faixa_salarial):
    df_filtered = df[df['Faixa salarial'] == faixa_salarial]

    df_count = df_filtered.groupby('uf onde mora')['Faixa salarial'].count().reset_index()
    df_count.columns = ['uf onde mora', 'Faixa salarial Count']

    geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

    fig = go.Figure(go.Choropleth(
        geojson=geojson_url,
        locations=df_count['uf onde mora'],
        z=df_count['Faixa salarial Count'],
        featureidkey="properties.sigla",
        colorscale="Viridis",
        marker_line_width=0.5,
        marker_line_color='white',
        colorbar_title="Contagem de Faixas Salariais",
    ))

    fig.update_geos(
        visible=False,
        fitbounds="locations",
        showcountries=True,
        countrycolor="Black",
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray"
    )

    fig.update_layout(
        title_text=f"Distribuição de '{faixa_salarial}' por Estado",
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="Black"
        )
    )

    return fig


def plot_mapa(df, faixa_salarial,genero):
    if genero == 'todos':
        df_filtered = df[df['Faixa salarial'] == faixa_salarial]
    else:
        df_filtered = df[(df['Faixa salarial'] == faixa_salarial) & (df['Genero'] == genero)]


    df_count = df_filtered.groupby('uf onde mora')['Faixa salarial'].count().reset_index()
    df_count.columns = ['uf onde mora', 'Faixa salarial Count']

    all_states = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    df_count = df_count.set_index('uf onde mora').reindex(all_states, fill_value=0).reset_index()

    geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

    fig = go.Figure(data=go.Choropleth(
        geojson=geojson_url,
        locations=df_count['uf onde mora'],
        z=df_count['Faixa salarial Count'],
        featureidkey="properties.sigla",
        colorscale=[[0, 'lightblue'], [1, 'darkblue']], 
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix='',
        colorbar_title='Faixa Salarial<br>Count',
    ))

    fig.update_geos(
        visible=False,
        fitbounds="locations",
        showcountries=True,
        countrycolor="Black",
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        projection_type='mercator',
        lonaxis_range=[-75, -30], 
        lataxis_range=[-35, 5], 
    )

    fig.update_layout(
        title_text=f"Distribuição da faixa salarial escolhida: <b>'{faixa_salarial}'<b> por Estado",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="Black",
            bgcolor='rgba(0,0,0,0)' 
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', 
        width=1000,
        height=700  
    )



    return fig


def plot_stacked_bar_percentage_salary_range_by_gender(df: DataFrame) -> None:
    """
    Plota um gráfico de barras empilhadas para Faixa Salarial por Gênero a partir de um DataFrame, mostrando porcentagens.

    :param df: DataFrame contendo os dados.
    """
    data_filtered = df.dropna(subset=['Genero', 'Faixa salarial'])
    
    total_por_genero = data_filtered.groupby('Genero').size()

    data_aggregated = data_filtered.groupby(['Faixa salarial', 'Genero']).size().reset_index(name='count')
    data_aggregated['percentage'] = data_aggregated.apply(lambda row: (row['count'] / total_por_genero[row['Genero']]) * 100, axis=1)

    faixa_salarial_order = [
    'Menos de R$ 1.000/mês',
    'de R$ 101/mês a R$ 2.000/mês ',
    'de R$ 1.001/mês a R$ 2.000/mês',
    'de R$ 2.001/mês a R$ 3.000/mês',
    'de R$ 3.001/mês a R$ 4.000/mês',
    'de R$ 4.001/mês a R$ 6.000/mês',
    'de R$ 6.001/mês a R$ 8.000/mês',
    'de R$ 8.001/mês a R$ 12.000/mês',
    'de R$ 12.001/mês a R$ 16.000/mês',
    'de R$ 16.001/mês a R$ 20.000/mês',
    'de R$ 20.001/mês a R$ 25.000/mês',
    'de R$ 25.001/mês a R$ 30.000/mês',
    'de R$ 30.001/mês a R$ 40.000/mês',
    'Acima de R$ 40.001/mês'
]
    
    color_dict = {
    'Masculino': '#0A77BE', 
    'Feminino': '#FF008E',
    }

    data_aggregated['Faixa salarial'] = pd.Categorical(data_aggregated['Faixa salarial'], categories=faixa_salarial_order, ordered=True)
    data_aggregated = data_aggregated.sort_values('Faixa salarial')
    fig = go.Figure()

    for gender in data_aggregated['Genero'].unique():
        df_gender = data_aggregated[data_aggregated['Genero'] == gender]
        fig.add_trace(go.Bar(
            x=df_gender['Faixa salarial'],
            y=df_gender['percentage'],
            name=gender,
            marker_color=color_dict[gender] 
        ))

    fig.update_layout(
        title='Faixa Salarial por Gênero (Proporções)',
        xaxis_title='Faixa Salarial',
        yaxis_title='Porcentagem',
        barmode='stack'
    )

    return fig


