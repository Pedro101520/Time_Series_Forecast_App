import pandas as pd
import streamlit as st
import altair as alt
from statsmodels.tsa.seasonal import seasonal_decompose
from utils.hipotese_adf import adf_test

def plot_series(df):
    df = df.copy()
    df["Data"] = pd.to_datetime(df["Data"])

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X("Data:T", title="Data"),
        y=alt.Y("Valor:Q", title="Valor"),
        tooltip=[
            alt.Tooltip("Data:T", title="Data", format="%Y-%m-%d %H:%M"),
            alt.Tooltip("Valor:Q", title="Valor", format=".2f")
        ],

        color=alt.Color("Tipo:N", title="Legenda") if "Tipo" in df.columns else alt.value("#4c78a8")
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

def exibe_painel():
    df = pd.DataFrame(st.session_state["historico_analitico"]["Serie_Temporal_Tratada_Analitico"])
    df["Data"] = pd.to_datetime(df["Data"])

    st.write("### Histórico da Série Temporal")

    plot_series(df)
    adf_test()

    st.divider()

    df.set_index("Data", inplace=True)
    df = df["Valor"]

    st.write("### Decomposição da Série Temporal")
    decomposition = seasonal_decompose(df, model='additive')
    fig = decomposition.plot()
    fig.set_size_inches(12, 8)
    st.pyplot(fig)
