import streamlit as st
import pandas as pd

def upload_arquivo():
    st.write("# Faça o upload de sua série temporal")

    st.write("")
    st.write("")
    st.write("")

    arquivo = st.file_uploader("Escolha a série temporal", type="csv", accept_multiple_files=False)
    if arquivo == None:
        st.warning("Por favor, envie um arquivo")
        return

    df = pd.read_csv(arquivo)