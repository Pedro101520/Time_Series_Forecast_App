import streamlit as st
from paginas.chatbot import renderiza_chat
from paginas.upload import upload_arquivo
from paginas.visao import exibe_painel
from paginas.outliers import box_plot

def botao_chat():
    st.session_state.chat = not st.session_state.chat

def carrega_pagina():
    if st.session_state.pagina == "Upload" and st.session_state.chat == False:
        upload_arquivo()
    elif st.session_state.pagina == "Visao" and st.session_state.chat == False:
        exibe_painel()
    elif st.session_state.pagina == "Outliers" and st.session_state.chat == False:
        box_plot()
    elif st.session_state.pagina == "Estacionariedade" and st.session_state.chat == False:
        st.write("Estacionariedade")
    elif st.session_state.pagina == "Forecast" and st.session_state.chat == False:
        st.write("Forecast")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Upload"

if "chat" not in st.session_state:
    st.session_state.chat = False

if "ok" not in st.session_state:
    st.session_state.ok = False

st.sidebar.write("# Navegação Forecast")
pagina = st.sidebar.selectbox("Navegação", ["1. Upload", "2. Visão Geral", "3. Outliers", "4. Estacionariedade", "5. Forecast"], disabled=st.session_state.chat or not(st.session_state.ok), label_visibility="collapsed")

if not(st.session_state.chat):
    match pagina:
        case "1. Upload":
            st.session_state.pagina = "Upload"
        case "2. Visão Geral":
            st.session_state.pagina = "Visao"
        case "3. Outliers":
            st.session_state.pagina = "Outliers"
        case "4. Estacionariedade":
            st.session_state.pagina = "Estacionariedade"
        case "5. Forecast":
            st.session_state.pagina = "Forecast"

texto_botao = "Forecast AI"
if st.session_state.chat == False:
    st.sidebar.button(
        texto_botao, 
        on_click=botao_chat,
        use_container_width=True
    )
else:
    st.sidebar.button(
        "Fechar Chat", 
        on_click=botao_chat,
        use_container_width=True
    )

if st.session_state.chat:
    renderiza_chat()
else:
    carrega_pagina()
