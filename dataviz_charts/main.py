import streamlit as st
import pandas as pd
from pandas import DataFrame
import re
import pandas as pd
import plotly.graph_objects as go
import base64
import os
from typing import List
from charts import (plot_age_distribution_by_gender,
                    plot_age_distribution_with_proportions_by_gender,
                    plot_stacked_bar_percentage_education_level_by_gender,
                    plot_age_distribution_pie_chart, 
                    plot_stacked_bar_percentage_salary_range_by_gender,
                    clean_data,
                    plot_mapa)

path = 'dataviz_charts/data/State_of_data_BR_2023_Kaggle - df_survey_2023.csv'
data = pd.read_csv(path)
st.set_page_config(layout="wide")
df_clean = clean_data(data)

options = st.sidebar.radio('Trabalho de Visualização de dados:', ['Sobre','Salário','Idade', 'Educação'])

if options == 'Sobre':
    st.markdown("""
    # Trabalho da disciplina Visualização de dados - PPGC
    ### Utilizando dados do State of Data, fazemos comparações entre gêneros.
    #### Grupo: Cassiano Michel, Emílio Bresolin, Marco Bochernitsan e Rodrigo Henrich
    #### Professora: Isabel Harb Manssour
                     
    Comparações realizadas no trabalho:
    - Idade
    - Educação
    - Salário
                

    ***Confira o [repositório no GitHub](https://github.com/marconb1/dataviz_masters) para mais informações.***
    """)
    _,col_title = st.columns([1, 1.9])
    with col_title: 

        script_directory = os.path.dirname(os.path.abspath(__file__))

        folder_path = os.path.join(script_directory, 'images')
        file_path = os.path.join(folder_path, 'date-everywhere-data.gif')
        file_ = open(file_path, "rb")

        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="data_gif">',
            unsafe_allow_html=True,
        )


if options == 'Idade':
    _,col_title,_ = st.columns([1,1, 1])
    with col_title: st.title("Distribuição de idades")
    

    st.markdown(
        """
        <style>
        .some-space {
            height: 40px; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="some-space"></div>', unsafe_allow_html=True)

    st.markdown("""Nesse primeiro gráfico temos números brutos, e entendemos que para uma melhor comparação, faz mais sentido normalizar as quantidades, visto que há aproximadamente 3x mais homens do que mulheres respondendo a pesquisa""")

    st.plotly_chart(plot_age_distribution_by_gender(df_clean),use_container_width=True)

    st.plotly_chart(plot_age_distribution_with_proportions_by_gender(df_clean),use_container_width=True)

    col1,col2 = st.columns ([1,1])

    with  col1:
        st.plotly_chart(plot_age_distribution_pie_chart(df_clean,'Masculino'),use_container_width=True)
    with  col2:
        st.plotly_chart(plot_age_distribution_pie_chart(df_clean,'Feminino'),use_container_width=True)

        
if options == 'Educação':
    _,col_title,_ = st.columns([1,1, 1])
    with col_title: st.title("Nível de ensino")

    st.plotly_chart (plot_stacked_bar_percentage_education_level_by_gender(df_clean),use_container_width=True)

if options == 'Salário':
    faixa_salarial_order = [
    'Menos de R$ 1.000/mês',
    'de R$ 101/mês a R$ 2.000/mês',
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
    'Acima de R$ 40.001/mês']
    _,col_title,_ = st.columns([1,1, 1])
    with col_title: st.title("Distribuição de salário por gênero")
    st.plotly_chart (plot_stacked_bar_percentage_salary_range_by_gender(df_clean),use_container_width=True)

    salary_category = st.selectbox("Selecione a Faixa Salarial", faixa_salarial_order, key="faixa_salarial")
    gen_selector = st.selectbox("Selecione o gênero", ['todos','Masculino','Feminino'], key="gen_selector")
    
    st.plotly_chart(plot_mapa(df_clean,salary_category,gen_selector),use_container_width=True,height=700)
