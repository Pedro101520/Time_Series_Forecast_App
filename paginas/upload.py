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
        "http://192.168.200.201:5000/pipeline/predicao", 
        files=files,
        headers=headers
    )

    if response.status_code == 200:
        payload = response.json()
        return payload
    else:
        erro = response.json()["erro"]
        erro_formatado = erro.encode("latin1").decode("unicode_escape")
        st.error(erro_formatado)
        st.stop()

def consumindo_api_analitico(arquivo):
    files = {"file": arquivo}

    load_dotenv()
    API_KEY = os.getenv("API_KEY_2")

    headers = {
        "x-api-key": API_KEY
    }

    response = requests.post(
        "http://192.168.200.201:5000/analitico", 
        files=files,
        headers=headers
    )

    if response.status_code == 200:
        payload = response.json()
        return payload
    
def consumindo_api_tratamento(arquivo):
    files = {"file": arquivo}

    load_dotenv()
    API_KEY = os.getenv("API_KEY_2")

    headers = {
        "x-api-key": API_KEY
    }

    response = requests.post(
        "http://192.168.200.201:5000/tratamento", 
        files=files,
        headers=headers
    )

    if response.status_code == 200:
        payload = response.json()
        return payload



def upload_arquivo():
    st.write("# Faça o upload de sua série temporal")

    st.write("")
    st.write("")
    st.write("")

    arquivo = st.file_uploader("Escolha a série temporal", type="csv", accept_multiple_files=False) 
    if arquivo == None:
        st.warning("Por favor, envie um arquivo")
        st.stop()
    elif st.session_state.ok and arquivo != None:
        st.success("Concluído")
        st.session_state.ok_mensagem = True
        st.stop()
    
    tamanho_mb = arquivo.size / (1024 * 1024)

    if tamanho_mb > 50:
        st.error("O arquivo deve ter no máximo 50MB.")
        st.stop()

    st.write("")
    st.write("")
    st.write("")

    if not(st.session_state.ok):
        with st.spinner("Aguarde...", show_time=True):
            dados_api = consumindo_api(arquivo)
            arquivo.seek(0)
            analitico = consumindo_api_analitico(arquivo)
            st.session_state["historico_analitico"] = analitico
            arquivo.seek(0)
            tratamento = consumindo_api_tratamento(arquivo)
            st.session_state["tratamento_sem_outliers"] = tratamento

        st.session_state.ok = True
        st.session_state["message"] = dados_api["message"]
        st.session_state["Melhor_Modelo"] = dados_api["Melhor Modelo"]
        st.session_state["Metricas"] = dados_api["Metricas"]
        st.session_state["Forecast"] = dados_api["Forecast"]
    st.rerun()