from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import Conversa
from app.db_config import db
from .forms import ChatbotForm
from .decorators import login_required, get_session_id
from .detections import detectar_emocao, detectar_distorcao
from app.utils.graficos import gerar_grafico_emocoes

chatbot_blueprint = Blueprint('chatbot', __name__)

@chatbot_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def chatbot():
    form = ChatbotForm()
    usuario_id = session.get('usuario_id')

    grafico_emocoes = gerar_grafico_emocoes(usuario_id, db)

    if form.validate_on_submit():
        mensagem = form.mensagem_usuario.data
        emocao = detectar_emocao(mensagem)
        distorcao = detectar_distorcao(mensagem)
        conversa = Conversa(
            usuario_id=usuario_id,
            mensagem_usuario=mensagem,
            mensagem_bo=f"Emoção: {emocao}, Distorção: {distorcao}"
        )
        db.session.add(conversa)
        db.session.commit()
        return redirect(url_for('chatbot.chatbot'))
    
    historico = Conversa.query.filter_by(usuario_id=usuario_id).all()
    return render_template('chatbot.html', form=form, historico=historico, usuario_logado=True, grafico_emocoes=grafico_emocoes)


@chatbot_blueprint.route('/demo', methods=['GET', 'POST'])
def chatbot_demo():
    form = ChatbotForm()
    session_id = get_session_id()
    if form.validate_on_submit():
        mensagem = form.mensagem_usuario.data
        emocao = detectar_emocao(mensagem)
        distorcao = detectar_distorcao(mensagem)
        resposta = f"Emoção: {emocao}, Distorção: {distorcao}"
        nova_conversa = Conversa(
            session_id=session_id,
            mensagem_usuario=mensagem,
            mensagem_bo=resposta
        )
        db.session.add(nova_conversa)
        db.session.commit()
        return redirect(url_for('chatbot.chatbot_demo'))
    historico = Conversa.query.filter_by(session_id=session_id, usuario_id=None).all()
    return render_template('chatbot_demo.html', form=form, historico=historico, usuario_logado=False, modo_demo=True)

@chatbot_blueprint.route('/demo/encerrar')
def encerrar_demo():
    session_id = session.pop('session_id', None)
    if session_id:
        Conversa.query.filter_by(session_id=session_id, usuario_id=None).delete()
        db.session.commit()
        flash('Sessão de demonstração encerrada.', 'info')
    return redirect(url_for('chatbot.chatbot_demo'))

