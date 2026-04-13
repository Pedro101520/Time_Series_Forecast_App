import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def calculos(valores):
    q1, mediana, q3 = np.percentile(valores, [25, 50, 75])
    iqr = q3 - q1
    whisker_low = valores[valores >= q1 - 1.5 * iqr].min()
    whisker_high = valores[valores <= q3 + 1.5 * iqr].max()
    outliers = valores[(valores < q1 - 1.5 * iqr) | (valores > q3 + 1.5 * iqr)]
    return q1, mediana, q3, whisker_low, whisker_high, outliers


def box_plot():
    df = pd.DataFrame(st.session_state["historico_analitico"]["Serie_Temporal_Tratada_Analitico"])

    valores = df["Valor"]
    q1, mediana, q3, whisker_low, whisker_high, outliers = calculos(valores)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Mín. (bigode)", f"{whisker_low:.2f}")
    col2.metric("Q1", f"{q1:.2f}")
    col3.metric("Mediana", f"{mediana:.2f}")
    col4.metric("Q3", f"{q3:.2f}")
    col5.metric("Máx. (bigode)", f"{whisker_high:.2f}")

    st.divider()

    st.write("### Box Plot")

    valores_normais = valores[~valores.isin(outliers)]

    fig, ax = plt.subplots(figsize=(10, 3))

    ax.boxplot(
        valores,
        vert=False,
        widths=0.5,
        patch_artist=True,
        boxprops=dict(facecolor="#cce5ff", color="#003f7f"),
        medianprops=dict(color="#ff6600", linewidth=2),
        whiskerprops=dict(color="#003f7f"),
        capprops=dict(color="#003f7f"),
        showfliers=False,
    )

    jitter_normais = np.random.uniform(0.85, 1.15, size=len(valores_normais))
    ax.scatter(valores_normais, jitter_normais, alpha=0.4, s=15, color="#1f77b4", zorder=3)

    margem = (whisker_high - whisker_low) * 0.1
    ax.set_xlim(whisker_low - margem, whisker_high + margem)

    if len(outliers) > 0:
        outliers_dir = outliers[outliers > whisker_high]
        outliers_esq = outliers[outliers < whisker_low]

        if len(outliers_dir) > 0:
            ax.annotate(
                f"  {len(outliers_dir)} outlier(s) ►",
                xy=(1, 0.5), xycoords="axes fraction",
                fontsize=9, color="red", va="center", ha="left"
            )

        if len(outliers_esq) > 0:
            ax.annotate(
                f"◄ {len(outliers_esq)} outlier(s)",
                xy=(0, 0.5), xycoords="axes fraction",
                fontsize=9, color="red", va="center", ha="right"
            )

    ax.set_yticks([])
    ax.set_xlabel("Valor")

    st.pyplot(fig)


def violin_plot():
    df = pd.DataFrame(st.session_state["historico_analitico"]["Serie_Temporal_Tratada_Analitico"])

    st.write("### Violin Plot")

    valores = df["Valor"]
    q1, mediana, q3, whisker_low, whisker_high, outliers = calculos(valores)

    valores_normais = valores[~valores.isin(outliers)]

    fig, ax = plt.subplots(figsize=(5, 7))

    parts = ax.violinplot(
        valores_normais,
        positions=[0],
        vert=True,
        showmedians=False,
        showextrema=False,
    )

    for pc in parts["bodies"]:
        pc.set_facecolor("#cce5ff")
        pc.set_edgecolor("#003f7f")
        pc.set_alpha(0.7)

    ax.vlines(0, whisker_low, whisker_high, color="#003f7f", linewidth=2, zorder=2)
    ax.fill_betweenx([q1, q3], -0.08, 0.08, color="#ff6600", alpha=0.6, zorder=3)
    ax.scatter([0], [mediana], color="white", s=60, zorder=5, edgecolors="#003f7f", linewidth=1.5)
    ax.hlines([whisker_low, whisker_high], -0.07, 0.07, color="#003f7f", linewidth=2, zorder=4)

    margem = (whisker_high - whisker_low) * 0.1
    ax.set_ylim(whisker_low - margem, whisker_high + margem)

    if len(outliers) > 0:
        outliers_cima = outliers[outliers > whisker_high]
        outliers_baixo = outliers[outliers < whisker_low]

        if len(outliers_cima) > 0:
            ax.annotate(
                f"▲ {len(outliers_cima)} outlier(s)",
                xy=(0.5, 1), xycoords="axes fraction",
                fontsize=9, color="red", va="bottom", ha="center"
            )

        if len(outliers_baixo) > 0:
            ax.annotate(
                f"▼ {len(outliers_baixo)} outlier(s)",
                xy=(0.5, 0), xycoords="axes fraction",
                fontsize=9, color="red", va="top", ha="center"
            )

    ax.set_xticks([])
    ax.set_ylabel("Valor")

    st.pyplot(fig)