import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def concatena(coluna):
    df_historico = pd.DataFrame(st.session_state["tratamento_sem_outliers"]["Serie_Temporal_Tratada"])
    df_forecast = pd.DataFrame(st.session_state["Forecast"])

    df_historico["Data"] = pd.to_datetime(df_historico["Data"])
    df_forecast[coluna] = pd.to_datetime(df_forecast[coluna])
    df_forecast[coluna] = pd.to_datetime(df_forecast[coluna])

    forecast = pd.concat([df_historico, df_forecast], axis=0)
    return forecast

def exibe_df(df):
    st.dataframe(df)

def infos():
    st.write(f"## Melhor modelo: {st.session_state["Melhor_Modelo"]}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"### RMSE: {float(st.session_state["Metricas"]["RMSE"])}")
    with col2:
        st.write(f"### MAE: {float(st.session_state["Metricas"]["MAE"])}")
    with col3:
        st.write(f"### MAPE: {float(st.session_state["Metricas"]["MAPE"])}")


def forecast_sarima():
    df = concatena("Data")

    historico = df[df["Valor_sem_outliers"].notna()]
    previsao  = df[df["forecast"].notna()]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=pd.concat([previsao["Data"], previsao["Data"][::-1]]),
        y=pd.concat([previsao["limite_superior"], previsao["limite_inferior"][::-1]]),
        fill="toself",
        fillcolor="rgba(55, 138, 221, 0.15)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=True,
        name="Intervalo de confiança",
    ))

    fig.add_trace(go.Scatter(
        x=historico["Data"],
        y=historico["Valor_sem_outliers"],
        mode="lines+markers",
        name="Histórico",
        line=dict(color="#1D9E75", width=2.5),
        marker=dict(size=5),
    ))

    fig.add_trace(go.Scatter(
        x=previsao["Data"],
        y=previsao["forecast"],
        mode="lines+markers",
        name="Forecast",
        line=dict(color="#378ADD", width=2.5, dash="dash"),
        marker=dict(size=5),
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
    st.divider()
    exibe_df(df)

def forecast_holt_winters():
    df_historico = pd.DataFrame(st.session_state["tratamento_sem_outliers"]["Serie_Temporal_Tratada"])
    df_forecast = pd.DataFrame(st.session_state["Forecast"])

    df_historico["Data"] = pd.to_datetime(df_historico["Data"])
    df_forecast["Data"] = pd.to_datetime(df_forecast["Data"])

    # Separa por data, não por .notna()
    ultima_data = df_historico["Data"].max()
    previsao = df_forecast[df_forecast["Data"] > ultima_data]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_historico["Data"],
        y=df_historico["Valor_sem_outliers"],
        mode="lines+markers",
        name="Histórico",
        line=dict(color="#1D9E75", width=2.5),
        marker=dict(size=5),
    ))

    fig.add_trace(go.Scatter(
        x=previsao["Data"],
        y=previsao["Valor"],
        mode="lines+markers",
        name="Forecast",
        line=dict(color="#378ADD", width=2.5, dash="dash"),
        marker=dict(size=5),
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
    st.divider()
    df_exibir = pd.concat([
        df_historico[["Data", "Valor_sem_outliers"]].rename(columns={"Valor_sem_outliers": "Valor"}),
        previsao[["Data", "Valor"]]
    ], ignore_index=True)
    exibe_df(df_exibir)


def forecast_prophet():
    df_historico = pd.DataFrame(st.session_state["tratamento_sem_outliers"]["Serie_Temporal_Tratada"])
    df_forecast = pd.DataFrame(st.session_state["Forecast"])

    df_historico["ds"] = pd.to_datetime(df_historico["Data"])
    df_forecast["ds"] = pd.to_datetime(df_forecast["ds"])

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    print(df_historico)


    ultima_data = df_historico["ds"].max()
    previsao = df_forecast[df_forecast["ds"] > ultima_data]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=pd.concat([previsao["ds"], previsao["ds"][::-1]]),
        y=pd.concat([previsao["yhat_upper"], previsao["yhat_lower"][::-1]]),
        fill="toself",
        fillcolor="rgba(55, 138, 221, 0.15)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=True,
        name="Intervalo de confiança",
    ))

    fig.add_trace(go.Scatter(
        x=df_historico["ds"],
        y=df_historico["Valor_sem_outliers"],
        mode="lines+markers",
        name="Histórico",
        line=dict(color="#1D9E75", width=2.5),
        marker=dict(size=5),
    ))

    fig.add_trace(go.Scatter(
        x=previsao["ds"],
        y=previsao["yhat"],
        mode="lines+markers",
        name="Forecast",
        line=dict(color="#378ADD", width=2.5, dash="dash"),
        marker=dict(size=5),
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
    st.divider()

    df_historico_exibir = df_historico[["ds", "Valor_sem_outliers"]].rename(columns={"ds": "Data", "Valor_sem_outliers": "Valor"}).copy()
    df_historico_exibir["Tipo"] = "Histórico"
    previsao_exibir = previsao[["ds", "yhat", "yhat_lower", "yhat_upper"]].rename(columns={"ds": "Data", "yhat": "Valor"}).copy()
    previsao_exibir["Tipo"] = "Forecast"
    df_exibir = pd.concat([df_historico_exibir, previsao_exibir], ignore_index=True)

    exibe_df(df_exibir)