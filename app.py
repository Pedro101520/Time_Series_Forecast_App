import streamlit as st
from paginas.chatbot import renderiza_chat
from paginas.upload import upload_arquivo

def botao_chat():
    st.session_state.clicked = True

st.sidebar.write("# Navegação Forecast")
pagina = st.sidebar.selectbox("Navegação", ["1. Upload", "2. Visão Geral", "3. Outliers", "4. Estacionariedade", "5. Forecast"], label_visibility="collapsed")


match pagina:
    case "1. Upload":
        upload_arquivo()
    case "2. Visão Geral":
        pass
    case "3. Outliers":
        pass
    case "4. Estacionariedade":
        pass
    case "5. Forecast":
        pass


if 'clicked' not in st.session_state:
    st.session_state.clicked = False

st.sidebar.button(
    "Forecast AI", 
    on_click=botao_chat,
    use_container_width=True
)

if st.session_state.clicked:
    renderiza_chat()
