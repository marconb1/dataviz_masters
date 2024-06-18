import pandas as pd
from pandas import DataFrame
import re
import pandas as pd
import plotly.graph_objects as go
from typing import List


pd.set_option('display.max_columns', None)



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

    df.columns = [extract_text_between_quotes(column_name)[1] for column_name in list(df.columns)]
    df = df[df['Genero'] != 'Prefiro não informar']
    df['Nivel de Ensino'] = df['Nivel de Ensino'].apply(substituir_nivel_ensino)
    df['Faixa salarial'] = df['Faixa salarial'].apply(lambda x: clean_salary_range(x) if pd.notna(x) else x)

    return df


def plot_age_distribution_by_gender(df: DataFrame) -> None:
    """
    Plota a distribuição de idade por gênero a partir de um arquivo CSV.

    :param path: Caminho para o arquivo CSV.
    :param encoding: Codificação do arquivo CSV.
    """
    data_filtered = df.dropna(subset=['Idade', 'Faixa idade', 'Genero'])

    data_aggregated = data_filtered.groupby(['Faixa idade', 'Genero']).size().reset_index(name='count')

    fig = go.Figure()

    for gender in data_aggregated['Genero'].unique():
        df_gender = data_aggregated[data_aggregated['Genero'] == gender]
        fig.add_trace(go.Bar(
            x=df_gender['Faixa idade'],
            y=df_gender['count'],
            name=gender
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

    for gender in data_aggregated['Genero'].unique():
        df_gender = data_aggregated[data_aggregated['Genero'] == gender]
        fig.add_trace(go.Bar(
            x=df_gender['Faixa idade'],
            y=df_gender['percentage'],
            name=gender
        ))

    fig.update_layout(
        title='Distribuição de Idade por Gênero (Proporções)',
        xaxis_title='Faixa de Idade',
        yaxis_title='Porcentagem',
        barmode='group'
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

    fig = go.Figure(data=[go.Pie(
        labels=data_aggregated['Faixa idade'],
        values=data_aggregated['count'],
        texttemplate='<b>%{label}</b><br>%{percent}',
        textinfo='percent+label',
        pull=[0.1 for _ in range(len(data_aggregated))],
        hole=0.4,
        sort=False
    )])

    fig.update_layout(
        title=f'Distribuição de Faixa de Idade para {genero}',
    )

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

    fig = go.Figure()

    for gender in data_aggregated['Genero'].unique():
        df_gender = data_aggregated[data_aggregated['Genero'] == gender]
        fig.add_trace(go.Bar(
            x=df_gender['Nivel de Ensino'],
            y=df_gender['percentage'],
            name=gender
        ))

    fig.update_layout(
        title='Nível de Ensino por Gênero (Proporções)',
        xaxis_title='Nível de Ensino',
        yaxis_title='Porcentagem',
        barmode='stack'
    )

    return fig


# prompt: utilizando nosso dataframe, criar agora a relação de faixa salarial por gênero

def plot_stacked_bar_percentage_salary_range_by_gender(df: DataFrame) -> None:
    """
    Plota um gráfico de barras empilhadas para Faixa Salarial por Gênero a partir de um DataFrame, mostrando porcentagens.

    :param df: DataFrame contendo os dados.
    """
    data_filtered = df.dropna(subset=['Genero', 'Faixa salarial'])

    total_por_genero = data_filtered.groupby('Genero').size()

    data_aggregated = data_filtered.groupby(['Faixa salarial', 'Genero']).size().reset_index(name='count')
    data_aggregated['percentage'] = data_aggregated.apply(lambda row: (row['count'] / total_por_genero[row['Genero']]) * 100, axis=1)

    fig = go.Figure()

    for gender in data_aggregated['Genero'].unique():
        df_gender = data_aggregated[data_aggregated['Genero'] == gender]
        fig.add_trace(go.Bar(
            x=df_gender['Faixa salarial'],
            y=df_gender['percentage'],
            name=gender
        ))

    fig.update_layout(
        title='Faixa Salarial por Gênero (Proporções)',
        xaxis_title='Faixa Salarial',
        yaxis_title='Porcentagem',
        barmode='stack'
    )

    return fig


