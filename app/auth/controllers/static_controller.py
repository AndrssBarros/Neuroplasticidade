from flask import render_template

def inicio():
    return render_template('inicio.html')
    
def distorcoes():
    return render_template('distorcoesCognitivas.html')


def exercicios():
    exercicios = [
        {"titulo": "Registro de Pensamentos", "descricao": "Identifique pensamentos automáticos diários.", "missao": "+5 por pensamento / +10 por distorção identificada"},
        {"titulo": "Diário de Emoções", "descricao": "Registre emoções sentidas em cada interação.", "missao": "+1 por emoção / +5 se complexa"},
        {"titulo": "Reestruturação Cognitiva", "descricao": "Desafie pensamentos e crie alternativas realistas.", "missao": "+10 por ciclo completo"},
        {"titulo": "Exposição Gradual", "descricao": "Enfrente situações que causam medo, de forma progressiva.", "missao": "+XP por desafio cumprido"},
        {"titulo": "Atividades Prazerosas", "descricao": "Faça ações que aumentam bem-estar e motivação.", "missao": "+10 por atividade"},
        {"titulo": "Acompanhamento de Hábitos", "descricao": "Monitore hábitos positivos com consistência.", "missao": "Bônus por sequência de 3+ dias"},
        {"titulo": "Cartas de Enfrentamento", "descricao": "Crie estratégias práticas para momentos de crise.", "missao": "Use no momento certo"},
        {"titulo": "Comunicação Assertiva", "descricao": "Pratique pedidos e críticas respeitosas.", "missao": "+XP por conversa real"},
        {"titulo": "Distorções Cognitivas", "descricao": "Detecte erros de pensamento nos seus relatos.", "missao": "+2 por acerto"},
        {"titulo": "Roda do Autocuidado", "descricao": "Aja em áreas como sono, lazer, físico, mental...", "missao": "Complete 6 áreas por semana"},
    ]
    return render_template('exercicios.html', exercicios=exercicios)

def dados():
    return render_template('dados.html')
