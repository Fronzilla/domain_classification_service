from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import streamlit as st

import scr.session_state as session
from scr.data import load_data
from scr.download import csv_download_link
from scr.model import load_model, predict
from scr.scrapper import scrap_data

st.set_page_config(page_title='Domain classification', layout='wide')


def main():
    session_state = session.get(df_data=None, domain_column=None, encoder=None, model=None)
    st.header("""Сервис классификации доменов""")

    st.sidebar.header('Классификация доменов по их содержимому (описанию)')
    st.sidebar.subheader('FAQ')

    with st.sidebar.beta_expander('Как использовать?'):
        st.write("""
                1. Загрузите файл следующих форматов:
                    - 'csv' 
                    - 'xlsx'
                2. Укажите название колонки, в которой находится целевая переменная (домен)
        """)

    with st.sidebar.beta_expander('Как интерпретировать результат?'):
        st.write(""" 
                - Результат работы модели - файл  .csv с двумя колонками:
                    - domain
                    - prediction
                - Если в prediction находится 1 - значит домен прошел классификацию, если 0 - нет
        """)

    with st.sidebar.beta_expander('Какие домены проходят классификацию?'):
        st.write(""" 
                    - Любые домены, со следующей тематикой, не проходят классификацию:
                        -  порнография, контент сексуальной направленности, «товары для взрослых»
                        - продажа товаров нарушающие законные права и интересы третьих лиц, 
                        в том числе права интеллектуальной собственности, авторские и смежные права
                        - продажа рецептурных медицинских препаратов и биологически активных добавок (БАД)
                        -  продажа любого типа алкоголя
                        - продажа табака, табачной продукции, 
                        сигарет (в том числе различного рода электронных и наполнителей для них)
                        - продажа наркотических средств, психотропных веществ, их прекурсоров 
                        или их аналогов, инструкции по их изготовлению, употреблению и/или сбыту
                        - услуги, связанные с предоставлением услуг проституции
                        - продажа/покупка любых ценных бумаг
                        - «финансовые пирамиды», Forex, букмекерские конторы
                        - обмен валюты
                        - продажа инструкции по изготовлению взрывчатых веществ, взрывных устройств, огнестрельного 
                        оружия (его частей), патронов или восстановление боевых свойств списанного огнестрельного оружия
                        - азартные игры (включая оплату фишек казино, сервисы азартных игр, онлайн казино, Лото), 
                        лотереи, а также букмекерские услуги 
                        (прием ставок, заключение пари на деньги или какую-либо материальную ценность)
                        - продажа баз данных, содержащих персональные данные и/или программное обеспечение, 
                        позволяющее обработку персональных данных в противоречие законодательству Российской Федерации
                        -  продажа реквизитов банковских карт и платный доступ к персональным данным 
                        (базы МТС, Билайн, МГТС, водительских прав и т.д.)
                        - продажа человеческих органов и останков
                        - б/у запчасти для автомобилей
                        - продажа особо ценных диких животных и их частей
                        - продажа товаров, распространение которых требует специальных разрешений, 
                        сертификатов и/или лицензий – без соответствующих разрешений, сертификатов и/или лицензий
                        - продажа товаров, распространение которых запрещено законодательством Российской Федерации
                        - 
                """)

    with st.sidebar.beta_expander('Почему в результатирующем файле доменов меньше, чем в исходном?'):
        st.write(""" 
                - Если контент домена определить не удалось - 
                он не будет учавствовать в классификации и , соотвественно, не попадет в результатирующий файл 
        """)

    load_data(session_state)  # загрузка данных в сессию
    load_model(session_state)  # загрузка модели в сессию

    if session_state.df_data is not None:
        domain_list = session_state.df_data[session_state.domain_column].to_list()
        st.write('Определенные домены')
        st.write(domain_list[0:10])
        st.write('...')

        result = {}

        with st.spinner('Определение содержимого доменов...'):
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {executor.submit(scrap_data, url): url for url in domain_list}
                for future in as_completed(futures):
                    url = futures[future]
                    result[url] = future.result()

        result = {k: v for k, v in result.items() if v}  # только домены с не пустым описанием
        if not result:
            st.error('Не удалось определить содержимое доменов, проверьте, правильно ли вы указали колонку')
            return

        with st.spinner('Классификация доменов...'):
            result_df = pd.DataFrame(result.items(), columns=['domain', 'description'])
            result_df['prediction'] = result_df['description'].apply(predict, args=(session_state,))
            result_df = result_df[['domain', 'prediction']]

        st.write('Классифицированные домены')
        st.write(result_df.head())
        st.write('...')

        st.write('Ссылка на скачивание')
        csv_download_link(result_df)


if __name__ == '__main__':
    main()
