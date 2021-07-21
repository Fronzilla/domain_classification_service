"""
Download results.
"""

import base64
import gzip
import io

import streamlit as st


def csv_download_link(df, sidebar=False, name='domains', compress=False):
    if compress:
        csv_buffer = io.StringIO()

        with gzip.GzipFile(mode='w', fileobj=csv_buffer) as gz_file:
            csv = df.to_csv(gz_file, index=False, compression='gzip')
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{name}">Download {name}</a>'

    else:
        csv = df.to_csv(index=False)
        name = f'{name}.csv'
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{name}">Download {name}</a>'

    if sidebar:
        st.sidebar.markdown(href, unsafe_allow_html=True)
    else:
        st.markdown(href, unsafe_allow_html=True)
