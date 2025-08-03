import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from app.models import Conversa
import matplotlib
matplotlib.use('Agg')
# Ativa o estilo seaborn
sns.set_theme(style="whitegrid")  # ou "darkgrid", "ticks", "white", etc.

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10
})

def gerar_grafico_distorcoes(usuario_id, db):
    conversas = Conversa.query.filter_by(usuario_id=usuario_id).filter(Conversa.distorcao_id != None).all()

    # Verificar se conversas foram recuperadas
    print(f'Número de conversas com distorção: {len(conversas)}')

    if not conversas:
        plt.figure(figsize=(6, 4))
        plt.text(0.5, 0.5, 'Nenhuma Distorção Registrada',
                 ha='center', va='center', fontsize=14, color='gray')
        plt.axis('off')
        plt.tight_layout()
    else:
        distorcoes = {}
        for conversa in conversas:
            nome = conversa.distorcao.nome
            distorcoes[nome] = distorcoes.get(nome, 0) + 1

        categorias = list(distorcoes.keys())
        valores = list(distorcoes.values())

        plt.figure(figsize=(6, 4))
        bars = plt.barh(categorias, valores, color='#6c63ff')
        plt.title('Distorções Cognitivas Detectadas', color='#003f87')
        plt.xlabel('Frequência')
        plt.grid(axis='x', linestyle='--', alpha=0.4)

        for bar in bars:
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                     str(int(bar.get_width())), va='center', fontsize=10)

        plt.tight_layout()


def gerar_grafico_progresso(usuario_id, db):
    from datetime import datetime
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd
    import io
    import base64

    dados = pd.DataFrame([
        {"semana": "Semana 1", "distorcoes": 3, "exercicios": 2, "emocao": "Alegria"},
        {"semana": "Semana 2", "distorcoes": 1, "exercicios": 4, "emocao": "Tristeza"},
    ])

    fig, ax1 = plt.subplots(figsize=(6, 4))
    sns.set_theme(style="whitegrid")

    dados.plot(kind="bar", x="semana", y=["distorcoes", "exercicios"], ax=ax1)

    for i, row in dados.iterrows():
        ax1.text(i - 0.1, row["distorcoes"] + 0.1, f'{row["emocao"]}', color='gray', fontsize=9)

    plt.title("Resumo do Seu Progresso")
    plt.ylabel("Quantidade")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

from collections import Counter

def gerar_grafico_emocoes(usuario_id, db):
    conversas = db.session.query(Conversa).filter(Conversa.usuario_id == usuario_id).all()
    
    # Adiciona uma verificação para incluir conversas com 'usuario_id' NULL
    if not conversas:
        conversas = db.session.query(Conversa).filter(Conversa.usuario_id == None).all()

    if not conversas:
        plt.figure(figsize=(6, 4))
        plt.text(0.5, 0.5, 'Nenhuma emoção detectada',
                 ha='center', va='center', fontsize=14, color='gray')
        plt.axis('off')
        plt.tight_layout()
    else:
        nomes_emocoes = []
        for conversa in conversas:
            mensagem_bo = conversa.mensagem_bo.lower()
            if 'anger' in mensagem_bo:
                nomes_emocoes.append('Raiva')
            elif 'fear' in mensagem_bo:
                nomes_emocoes.append('Medo')
            elif 'joy' in mensagem_bo:
                nomes_emocoes.append('Alegria')
            elif 'sadness' in mensagem_bo:
                nomes_emocoes.append('Tristeza')
            elif 'surprise' in mensagem_bo:
                nomes_emocoes.append('Surpresa')
            elif 'neutral' in mensagem_bo:
                nomes_emocoes.append('Neutro')
            elif 'disgust' in mensagem_bo:
                nomes_emocoes.append('Desgosto')
            else:
                nomes_emocoes.append('Desconhecida')

        contagem = Counter(nomes_emocoes)

        emocoes = list(contagem.keys())
        valores = list(contagem.values())

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(emocoes, valores, color='skyblue')
        ax.set_title('Frequência de Emoções Detectadas')
        ax.set_ylabel('Ocorrências')
        plt.xticks(rotation=30)
        plt.tight_layout()

    # Codifica imagem em base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    return grafico_base64
