import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
from utils.hipotese_adf import adf_test

def plot_series(df):
    df["Data"] = pd.to_datetime(df["Data"])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Data"],
        y=df["Valor"],
        mode="lines+markers",
        name="Histórico",
        line=dict(color="#1D9E75", width=2.5),
        marker=dict(size=4),
    ))

    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(title="Data", showgrid=True, gridcolor="rgba(128,128,128,0.15)"),
        yaxis=dict(title="Valor", showgrid=True, gridcolor="rgba(128,128,128,0.15)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=40, l=10, r=10),
    )

    st.plotly_chart(fig, use_container_width=True)

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
