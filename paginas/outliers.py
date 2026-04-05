import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def box_plot():
    df = pd.DataFrame(st.session_state["historico_analitico"]["Serie_Temporal_Tratada_Analitico"])

    st.write("### Histórico da Série Temporal")

    valores = df['Valor']

    fig, ax = plt.subplots()
    
    ax.boxplot(valores, vert=False)

    y = np.random.normal(1, 0.04, size=len(valores))
    ax.scatter(valores, y, alpha=0.5)

    ax.set_title("Boxplot com pontos")
    ax.set_xlabel("Valor")

    st.pyplot(fig)