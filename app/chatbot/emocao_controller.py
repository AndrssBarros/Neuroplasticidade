import io
import base64
import matplotlib.pyplot as plt
from flask import render_template, Blueprint
from flask_login import current_user, login_required
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models import Conversa, EmocaoDetectada
from app.db_config import db

emocao_blueprint = Blueprint('emocao', __name__)

@emocao_blueprint.route('/emocoes', methods=['GET'])
@login_required
def registro_emocoes():
    hoje = datetime.utcnow()
    sete_dias_atras = hoje - timedelta(days=7)

    conversas_usuario = (
        db.session.query(EmocaoDetectada.nome_emocao, func.count().label('quantidade'))
        .join(Conversa, Conversa.emocao_id == EmocaoDetectada.emocao_id)
        .filter(Conversa.usuario_id == current_user.usuario_id)
        .filter(Conversa.data_interacao >= sete_dias_atras)
        .group_by(EmocaoDetectada.nome_emocao)
        .order_by(func.count().desc())
        .all()
    )

    if conversas_usuario:
        destaque_texto = f"Nas últimas interações, notamos um aumento em {conversas_usuario[0][0].lower()}."

        # Criar gráfico simples com Matplotlib
        nomes = [x[0] for x in conversas_usuario]
        quantidades = [x[1] for x in conversas_usuario]

        plt.figure(figsize=(8, 4))
        plt.bar(nomes, quantidades, color='skyblue')
        plt.title('Distribuição das Emoções')
        plt.xlabel('Emoções')
        plt.ylabel('Quantidade')
        plt.tight_layout()

        # Salvar em buffer e converter para base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        grafico_emocoes = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
    else:
        destaque_texto = "Ainda não há emoções detectadas nas suas interações recentes."
        grafico_emocoes = None

    return render_template("registroEmocoes.html", destaque_texto=destaque_texto, grafico_emocoes=grafico_emocoes)
