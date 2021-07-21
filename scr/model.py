import pickle

import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer


def load_model(session_state):
    with st.spinner('Загрузка модели машинного обучения...'):
        encoder = SentenceTransformer('distiluse-base-multilingual-cased')
    session_state.encoder = encoder
    session_state.model = pickle.load(open('models/multilingual_universal_sentence_encoder.pkl', 'rb'))


def encode(encoder, sents_list, pbar=True):
    embs = encoder.encode(sents_list, show_progress_bar=pbar)
    return np.array(embs)


def predict(sentence, session_state):
    return session_state.model.predict(encode(session_state.encoder, [sentence]))[0]
