import plotly.graph_objects as go
import numpy as np
import os

def gerar_roda_emocoes():
    emocoes = ["Alegria", "Confiança", "Antecipação", "Raiva", "Tristeza", "Medo", "Surpresa", "Repulsa"]
    valores = [0.7, 0.6, 0.5, 0.3, 0.4, 0.5, 0.6, 0.4]

    # Fecha o ciclo no gráfico
    emocoes += [emocoes[0]]
    valores += [valores[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=emocoes,
        fill='toself',
        name='Emoções',
        line_color='#003f87',  # Azul escuro do sistema
        fillcolor='rgba(0, 63, 135, 0.1)',  # Transparente suave
        marker=dict(color='#003f87')
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Fundo transparente
        plot_bgcolor='rgba(0,0,0,0)',
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=False
            ),
            angularaxis=dict(
                tickfont=dict(
                    size=13,
                    color='#444'  # Cinza escuro
                ),
                linecolor='rgba(0,0,0,0.1)',  # Linha sutil
                gridcolor='rgba(0,0,0,0.05)'  # Grade suave
            )
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    # Salva o gráfico
    path = os.path.join("static", "graficos", "roda_emocoes.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.write_html(path)
