import streamlit as st
from paginas.chatbot import renderiza_chat
from paginas.upload import upload_arquivo

def botao_chat():
    st.session_state.chat = not st.session_state.chat

def carrega_pagina():
    if st.session_state.pagina == "Upload" and st.session_state.chat == False:
        upload_arquivo()
    if st.session_state.pagina == "Visao" and st.session_state.chat == False:
        st.write("Visao")
    if st.session_state.pagina == "Outliers" and st.session_state.chat == False:
        st.write("Outliers")
    if st.session_state.pagina == "Estacionariedade" and st.session_state.chat == False:
        st.write("Estacionariedade")
    if st.session_state.pagina == "Forecast" and st.session_state.chat == False:
        st.write("Forecast")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Upload"

if "chat" not in st.session_state:
    st.session_state.chat = False

st.sidebar.write("# Navegação Forecast")
pagina = st.sidebar.selectbox("Navegação", ["1. Upload", "2. Visão Geral", "3. Outliers", "4. Estacionariedade", "5. Forecast"], disabled=st.session_state.chat, label_visibility="collapsed")

estado = None
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

carrega_pagina()

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
