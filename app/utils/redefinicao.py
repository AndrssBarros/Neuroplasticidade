from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.ext import mail  

def gerar_token_redefinicao(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='senha-redefinicao')

def verificar_token_redefinicao(token, tempo_expiracao=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='senha-redefinicao', max_age=tempo_expiracao)
        return email
    except Exception as e:
        print(f"[Token inválido]: {e}")
        return None

def enviar_email_redefinicao(usuario):
    token = gerar_token_redefinicao(usuario.email)
    link = url_for('auth.resetar_senha', token=token, _external=True)
    msg = Message(
        subject='Redefinição de Senha',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[usuario.email],
        body=f'Clique no link para redefinir sua senha: {link}'
    )
    mail.send(msg)
