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
        st.write(f"### RMSE: {float(st.session_state["Metricas"]["RMSE"]):.2f}")
    with col2:
        st.write(f"### MAE: {float(st.session_state["Metricas"]["MAE"]):.2f}")
    with col3:
        st.write(f"### MAPE: {(float(st.session_state["Metricas"]["MAPE"])*100):.2f}%")


def forecast_sarima():
    df_historico = pd.DataFrame(
        st.session_state["tratamento_sem_outliers"]["Serie_Temporal_Tratada"]
    )
    df_forecast = pd.DataFrame(st.session_state["Forecast"])

    df_historico["Data"] = pd.to_datetime(df_historico["Data"])
    df_forecast["Data"] = pd.to_datetime(df_forecast["Data"])

    qtd_linhas = len(df_historico)
    inicio_30 = int(qtd_linhas * 0.70)
    df_historico_filtro = df_historico.iloc[inicio_30:].copy()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=pd.concat([df_forecast["Data"], df_forecast["Data"][::-1]]),
        y=pd.concat([
            df_forecast["limite_superior"],
            df_forecast["limite_inferior"][::-1]
        ]),
        fill="toself",
        fillcolor="rgba(55, 138, 221, 0.15)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=True,
        name="Intervalo de confiança",
    ))

    fig.add_trace(go.Scatter(
        x=df_historico_filtro["Data"],
        y=df_historico_filtro["Valor_sem_outliers"],
        mode="lines+markers",
        name="Histórico",
        line=dict(color="#1D9E75", width=2.5),
        marker=dict(size=5),
    ))

    fig.add_trace(go.Scatter(
        x=df_forecast["Data"],
        y=df_forecast["forecast"],
        mode="lines+markers",
        name="Forecast",
        line=dict(color="#378ADD", width=2.5, dash="dash"),
        marker=dict(size=5)
    ))

    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(
            title="Data",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.15)"
        ),
        yaxis=dict(
            title="Valor",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.15)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=40, l=10, r=10),
    )

    st.plotly_chart(fig, use_container_width=True)

    df_forecast = df_forecast.rename(columns={"forecast":"Valor"})
    df_historico = df_historico.drop(columns="Valor_sem_outliers")
    df_historico["Tipo"] = "Histórico"
    df_forecast["Tipo"] = "Forecast"
    df_exibir = pd.concat([df_historico, df_forecast], ignore_index=True)
    exibe_df(df_exibir)


def forecast_holt_winters():
    df_historico = pd.DataFrame(st.session_state["tratamento_sem_outliers"]["Serie_Temporal_Tratada"])
    df_forecast = pd.DataFrame(st.session_state["Forecast"])

    df_historico["Data"] = pd.to_datetime(df_historico["Data"])
    df_forecast["Data"] = pd.to_datetime(df_forecast["Data"])

    qtd_linhas = len(df_historico)
    inicio_30 = int(qtd_linhas * 0.70)
    df_historico_filtro = df_historico.iloc[inicio_30:].copy()

    ultima_data = df_historico["Data"].max()
    previsao = df_forecast[df_forecast["Data"] > ultima_data]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_historico_filtro["Data"],
        y=df_historico_filtro["Valor_sem_outliers"],
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
    df_historico["Tipo"] = "Histórico"
    previsao["Tipo"] = "Forecast"
    df_exibir = pd.concat([
        df_historico[["Data", "Valor_sem_outliers", "Tipo"]].rename(columns={"Valor_sem_outliers": "Valor"}),
        previsao[["Data", "Valor", "Tipo"]]
    ], ignore_index=True)
    exibe_df(df_exibir)


def forecast_prophet():
    df_historico = pd.DataFrame(st.session_state["tratamento_sem_outliers"]["Serie_Temporal_Tratada"])
    df_forecast = pd.DataFrame(st.session_state["Forecast"])

    df_historico["ds"] = pd.to_datetime(df_historico["Data"])
    df_forecast["ds"] = pd.to_datetime(df_forecast["ds"])

    qtd_linhas = len(df_historico)
    inicio_30 = int(qtd_linhas * 0.70)
    df_historico_filtro = df_historico.iloc[inicio_30:].copy()

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    ultima_data = df_historico_filtro["ds"].max()
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
        x=df_historico_filtro["ds"],
        y=df_historico_filtro["Valor_sem_outliers"],
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