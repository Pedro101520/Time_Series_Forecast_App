import streamlit as st
import pandas as pd
import requests

from dotenv import load_dotenv
import os


def consumindo_api(arquivo):
    files = {"file": arquivo}

    load_dotenv()
    API_KEY = os.getenv("API_KEY_2")

    headers = {
        "x-api-key": API_KEY
    }

    response = requests.post(
        "https://forecast-api-563570939574.southamerica-east1.run.app/pipeline/predicao", 
        files=files,
        headers=headers
    )

    if response.status_code == 200:
        payload = response.json()
        return payload
    else:
        st.error(f"Erro na API: {response.status_code}")
        st.text(response.text)
        st.stop()



def upload_arquivo():
    st.write("# Faça o upload de sua série temporal")

    st.write("")
    st.write("")
    st.write("")

    arquivo = st.file_uploader("Escolha a série temporal", type="csv", accept_multiple_files=False)
    if arquivo == None:
        st.warning("Por favor, envie um arquivo")
        st.stop()
    
    tamanho_mb = arquivo.size / (1024 * 1024)

    if tamanho_mb > 50:
        st.error("O arquivo deve ter no máximo 50MB.")
        st.stop()

    st.write("")
    st.write("")
    st.write("")

    with st.spinner("Aguarde...", show_time=True):
        dados_api = consumindo_api(arquivo)
    st.success("Concluído")
    st.button("Executar Novamente")

    st.session_state["message"] = dados_api["message"]
    st.session_state["Melhor_Modelo"] = dados_api["Melhor Modelo"]
    st.session_state["Metricas"] = dados_api["Metricas"]
    st.session_state["Forecast"] = dados_api["Forecast"]