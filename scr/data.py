from typing import NoReturn

import pandas as pd
import streamlit as st


def load_data(session_state) -> NoReturn:
    st.subheader('Загрузка данных')
    st.write("""Загрузите 'csv' или 'xlsx' файл с одним листом.
             Домены должны быть в колонке domain, либо укажите название колонки с доменами.""")

    data_file = st.file_uploader("Файл форматов 'csv', 'xlsx' ", type=['csv', 'xlsx'])
    domain_column = st.text_input('Укажите названи колонки доменами', value='domain')

    if data_file is not None:

        df_data = pd.read_csv(data_file).head(10)
        st.write(df_data.head())

        if domain_column not in df_data.columns:
            st.warning(f'Домены должны быть в колонке {domain_column}.')
            return

        df_data = df_data[~df_data[domain_column].isna()]

        session_state.df_data = df_data
        session_state.domain_column = domain_column
