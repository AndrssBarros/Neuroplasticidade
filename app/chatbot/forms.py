import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from email_validator import validate_email, EmailNotValidError

class ChatbotForm(FlaskForm):
    mensagem_usuario = StringField('Mensagem', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired()])  # Removido Email()
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Cadastre-se')
    aceita_termos = BooleanField('Aceito os Termos', validators=[DataRequired()])

    def validate_password(self, field):
        senha = field.data
        print(f"[DEBUG] Validando senha: {senha}")
        if not re.search(r'[A-Z]', senha):
            print("[DEBUG] Falhou: precisa de letra maiúscula")
            raise ValidationError('A senha deve conter ao menos uma letra maiúscula.')
        if not re.search(r'[a-z]', senha):
            print("[DEBUG] Falhou: precisa de letra minúscula")
            raise ValidationError('A senha deve conter ao menos uma letra minúscula.')
        if not re.search(r'\d', senha):
            print("[DEBUG] Falhou: precisa de número")
            raise ValidationError('A senha deve conter ao menos um número.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            print("[DEBUG] Falhou: precisa de caractere especial")
            raise ValidationError('A senha deve conter ao menos um caractere especial.')

    def validate_email(self, field):
        try:
            validate_email(field.data) 
        except EmailNotValidError as e:
            print(f"[DEBUG] Email inválido: {e}")
            raise ValidationError('Insira um email válido.')
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])

class SolicitarRedefinicaoForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar link de redefinição')

class RedefinirSenhaForm(FlaskForm):
    senha = PasswordField('Nova Senha', validators=[DataRequired()])
    confirmar = PasswordField('Confirmar Senha', validators=[
        DataRequired(), EqualTo('senha', message='As senhas devem coincidir.')
    ])
    submit = SubmitField('Redefinir Senha')
