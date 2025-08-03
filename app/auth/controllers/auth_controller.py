from flask import render_template, request, flash, redirect, url_for, session
from app.models import Usuario, Exercicio
from app.chatbot.forms import LoginForm, RegistrationForm, SolicitarRedefinicaoForm, RedefinirSenhaForm
from app.chatbot.utils import verificar_token_redefinicao
from app.utils.redefinicao import enviar_email_redefinicao
from app.db_config import db
from app.utils.graficos import gerar_grafico_distorcoes
from flask_login import login_user, current_user
import re

def validar_senha(senha):
    erros = []
    if len(senha) < 8:
        erros.append('len')
    if not re.search(r'[A-Z]', senha):
        erros.append('maiuscula')
    if not re.search(r'[0-9]', senha):
        erros.append('numero')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        erros.append('especial')
    return erros

def cadastro():
    form = RegistrationForm()
    if form.validate_on_submit():
        if not request.form.get('aceita_termos'):
            flash('Você deve aceitar os Termos e Condições para continuar.', 'error')
            return redirect(url_for('auth.cadastro'))

        # Verificando se o e-mail já está cadastrado
        if Usuario.query.filter_by(email=form.email.data).first():
            flash('Este e-mail já está cadastrado. Tente outro.', 'danger')
            return render_template('cadastro.html', form=form)

        erros_senha = validar_senha(form.password.data)
        if erros_senha:
            flash('A senha não atende a todos os critérios.', 'danger')
            return render_template('cadastro.html', form=form, erros_senha=erros_senha)

        usuario = Usuario(email=form.email.data, nome_usuario=form.nome.data)
        usuario.set_password(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html', form=form, erros_senha=[])


def login():
    form = LoginForm() 
    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            flash('Este e-mail não está cadastrado.', 'danger')
        elif not usuario.check_password(senha):
            flash('Senha incorreta. Tente novamente.', 'danger')
        else:
            login_user(usuario)
            return redirect(url_for('auth.logado'))

    return render_template('login.html', form=form)

def solicitar_redefinicao():
    form = SolicitarRedefinicaoForm()
    if form.validate_on_submit():
        email = form.email.data
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            try:
                enviar_email_redefinicao(usuario)
                flash('Um link de redefinição foi enviado para o seu e-mail.', 'success')
            except Exception as e:
                print(f"[ERRO] Falha ao enviar e-mail: {e}")
                flash('Erro ao enviar o e-mail. Tente novamente mais tarde.', 'danger')
        else:
            flash('Se o e-mail estiver cadastrado, você receberá um link de redefinição.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('solicitar_redefinicao.html', form=form)

def redefinir_senha(token):
    email = verificar_token_redefinicao(token)
    if not email:
        flash('O link de redefinição é inválido ou expirou.', 'danger')
        return redirect(url_for('auth.login'))

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.login'))

    form = RedefinirSenhaForm()
    if form.validate_on_submit():
        nova_senha = form.senha.data
        usuario.set_password(nova_senha)
        db.session.commit()
        flash('Sua senha foi atualizada com sucesso!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('resetar_senha.html', form=form)
def logado():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))  # Redireciona para a tela de login se não estiver autenticado

    usuario_id = current_user.usuario_id  # Alteração aqui
    nome_usuario = current_user.nome_usuario

    grafico_distorcoes = gerar_grafico_distorcoes(usuario_id, db)
    exercicios = Exercicio.query.filter_by(usuario_id=usuario_id).order_by(Exercicio.data_criacao.desc()).all()

    return render_template(
        'logado.html',
        nome_usuario=nome_usuario,
        grafico_distorcoes=grafico_distorcoes,
        exercicios=exercicios
    )
