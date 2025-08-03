from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Usuario
from app.db_config import db  
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_required

configuracoes = Blueprint('configuracoes', __name__, url_prefix='/configuracoes')

@login_required
@configuracoes.route('/', methods=['GET', 'POST'])
def pagina_configuracoes():
    return render_template('configuracoes.html')


@configuracoes.route('/alterar-dados', methods=['POST'])
def alterar_dados():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para alterar seus dados.', 'error')
        return redirect(url_for('auth.login'))

    nome = request.form.get('nome')
    email = request.form.get('email')

    if not nome or not email:
        flash('Por favor, preencha todos os campos.', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

    usuario = Usuario.query.get(current_user.usuario_id)

    if usuario:
        usuario.nome_usuario = nome
        usuario.email = email
        try:
            db.session.commit()
            flash('Dados alterados com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao atualizar os dados: {str(e)}', 'error')
    else:
        flash('Usuário não encontrado.', 'error')

    return redirect(url_for('configuracoes.pagina_configuracoes'))


@configuracoes.route('/alterar-senha', methods=['POST'])
def alterar_senha():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para alterar sua senha.', 'error')
        return redirect(url_for('auth.login'))

    senha_atual = request.form.get('senha_atual')
    senha_nova = request.form.get('senha_nova')
    senha_repete = request.form.get('senha_repete')

    if not senha_atual or not senha_nova or not senha_repete:
        flash('Por favor, preencha todos os campos.', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

    if senha_nova != senha_repete:
        flash('As novas senhas não coincidem.', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

    if senha_nova == senha_atual:
        flash('A nova senha deve ser diferente da atual.', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

    if len(senha_nova) < 8:
        flash('A senha deve ter pelo menos 8 caracteres.', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

    usuario = Usuario.query.get(current_user.usuario_id)

    if not usuario:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

    if not usuario.check_password(senha_atual):
        flash('Senha atual incorreta.', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

    try:
        usuario.senha = generate_password_hash(senha_nova)
        db.session.commit()
        flash('Senha alterada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao alterar a senha: {str(e)}', 'error')

    return redirect(url_for('configuracoes.pagina_configuracoes'))


@configuracoes.route('/notificacoes', methods=['POST'])
def notificacoes():
    if request.method == 'POST':
        lembretes_email = 'lembretes_email' in request.form
        atualizacoes_sistema = 'atualizacoes_sistema' in request.form


        flash('Preferências de notificação atualizadas!', 'success')
    return redirect(url_for('configuracoes.pagina_configuracoes'))


@configuracoes.route('/resetar-conversas', methods=['POST'])
def resetar_conversas():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('auth.login'))

    usuario_id = session['usuario_id']
    try:
        conversa.query.filter_by(usuario_id=usuario_id).delete()
        db.session.commit()
        flash('Todas as conversas foram apagadas.', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro: {e}', 'error')

    return redirect(url_for('configuracoes.pagina_configuracoes'))



@configuracoes.route('/apagar-conta', methods=['POST'])
def apagar_conta():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Você precisa estar logado para apagar a conta.', 'error')
        return redirect(url_for('auth.login'))

    senha_confirmacao = request.form.get('senha_confirmacao')
    if not senha_confirmacao:
        flash('Por favor, informe a senha para confirmar a exclusão.', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

    usuario = Usuario.query.filter_by(usuario_id=usuario_id).first()
    if not usuario:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

    if not usuario.check_password(senha_confirmacao):
        flash('Senha incorreta. Exclusão cancelada.', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

    try:
        db.session.delete(usuario)
        db.session.commit()
        session.clear()
        flash('Conta apagada com sucesso.', 'danger')
        return redirect(url_for('auth.inicio'))
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao apagar a conta: {str(e)}', 'error')
        return redirect(url_for('configuracoes.pagina_configuracoes'))

@configuracoes.route('/alterar-tema', methods=['POST'])
def alterar_tema():
    novo_tema = request.form.get('tema')
    session['tema'] = novo_tema  

    usuario = Usuario.query.get(current_user.usuario_id)
    if usuario:
        usuario.tema = novo_tema
        try:
            db.session.commit()
            flash('Tema atualizado!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar o tema: {str(e)}', 'error')

    return redirect(url_for('configuracoes.pagina_configuracoes'))

@configuracoes.route('/alterar-fonte', methods=['POST'])
def alterar_fonte():
    if request.method == 'POST':
        session['tamanho_fonte'] = request.form.get('tamanho_fonte')
        flash('Fonte atualizada!', 'success')
    return redirect(url_for('configuracoes.pagina_configuracoes'))
