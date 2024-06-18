import streamlit as st
import pandas as pd
from pandas import DataFrame
import re
import pandas as pd
import plotly.graph_objects as go
from typing import List
from charts import (plot_age_distribution_by_gender,
                    plot_age_distribution_with_proportions_by_gender,
                    plot_stacked_bar_percentage_education_level_by_gender,
                    plot_age_distribution_pie_chart, 
                    plot_stacked_bar_percentage_salary_range_by_gender,
                    clean_data)

path = 'dataviz_charts/data/State_of_data_2022.csv'
data = pd.read_csv(path)
st.set_page_config(layout="wide")
df_clean = clean_data(data)

options = st.sidebar.radio('DataViz: Data Gender Study:', ['Age Distribution', 'Education level', 'Salary Distribution'])

if options == 'Age Distribution':
    _,col_title = st.columns([1, 1.2])
    with col_title: st.title("Age Distribution")

    st.plotly_chart(plot_age_distribution_by_gender(df_clean),use_container_width=True)

    st.plotly_chart(plot_age_distribution_with_proportions_by_gender(df_clean),use_container_width=True)

    col1,col2 = st.columns ([1,1])

    with  col1:
        st.plotly_chart(plot_age_distribution_pie_chart(df_clean,'Masculino'),use_container_width=True)
    with  col2:
        st.plotly_chart(plot_age_distribution_pie_chart(df_clean,'Feminino'),use_container_width=True)

        
if options == 'Education level':
    _,col_title = st.columns([1, 1.2])
    with col_title: st.title("Education Level")

    st.plotly_chart (plot_stacked_bar_percentage_education_level_by_gender(df_clean),use_container_width=True)

if options == 'Salary Distribution':
     _,col_title = st.columns([1, 1.2])
     with col_title: st.title("Salary Distribution")
     st.plotly_chart (plot_stacked_bar_percentage_salary_range_by_gender(df_clean),use_container_width=True)