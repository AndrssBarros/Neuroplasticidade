from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from app.db_config import db
from app.models import Exercicio
from app.chatbot.decorators import login_required

exercicio_bp = Blueprint('exercicio', __name__)

@login_required
@exercicio_bp.route('/enviar-exercicio', methods=['POST'])

def enviar_exercicio():
    texto = request.form.get('texto')
    usuario_id = session.get('usuario_id')

    if not texto:
        flash('O exercício está vazio.', 'warning')
        return redirect(url_for('auth.logado'))

    novo_exercicio = Exercicio(texto=texto, usuario_id=usuario_id)
    db.session.add(novo_exercicio)
    db.session.commit()

    flash('Exercício enviado com sucesso!', 'success')
    return redirect(url_for('auth.logado'))
