from statsmodels.tsa.stattools import adfuller
import pandas as pd
import streamlit as st

def adf_test():
    df = pd.DataFrame(st.session_state["historico_analitico"]["Serie_Temporal_Tratada_Analitico"])
    result = adfuller(df["Valor"])

    st.write("### Teste de Estacionariedade (ADF)")

    if result[1] <= 0.05:
        st.write(f"""
        **Série estacionária**

        O teste ADF resultou em **p-value = {result[1]:.4f}**, indicando rejeição da hipótese nula.  
        Isso significa que a série possui propriedades estatísticas estáveis ao longo do tempo.
        """)
    else:
        st.write(f"""
        **Série não estacionária**

        O teste ADF resultou em **p-value = {result[1]:.4f}**, indicando que não foi possível rejeitar a hipótese nula.  
        Isso sugere que a série apresenta variações estruturais ao longo do tempo.
        """)
