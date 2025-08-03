from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from datetime import datetime
from .db_config import db


def get_fernet():
    return Fernet(current_app.config['FERNET_KEY'].encode())


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), nullable=True)
    nome_usuario = db.Column(db.String(50), nullable=False)

    email = db.Column('email', db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    data_registro = db.Column(db.DateTime)
    tema = db.Column(db.String(20), default='claro')
    tamanho_fonte = db.Column(db.String(10), default='normal')

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    def get_id(self):
        return str(self.usuario_id)

class EmocaoDetectada(db.Model):
    __tablename__ = 'emocoes_detectadas'

    emocao_id = db.Column(db.Integer, primary_key=True)
    nome_emocao = db.Column(db.Text, nullable=False)
    tipo_emocao = db.Column(db.Text, nullable=False)


class DistorcaoCognitiva(db.Model):
    __tablename__ = 'distorcao_cognitiva'

    distorcao_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text, nullable=False)


class QuestionamentoSocratico(db.Model):
    __tablename__ = 'questionamento_socratico'

    questionamento_id = db.Column(db.Integer, primary_key=True)
    texto_pergunta = db.Column(db.Text, nullable=False)
    distorcao_id = db.Column(db.Integer, db.ForeignKey('distorcao_cognitiva.distorcao_id'), nullable=False)

    distorcao = db.relationship('DistorcaoCognitiva', backref='questionamentos')


class Conversa(db.Model):
    __tablename__ = 'conversa'

    conversa_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=True)
    session_id = db.Column(db.String(64), nullable=True)

    _mensagem_usuario = db.Column('mensagem_usuario', db.Text, nullable=False)
    mensagem_bo = db.Column(db.Text)
    data_interacao = db.Column(db.DateTime, default=db.func.current_timestamp())

    emocao_id = db.Column(db.Integer, db.ForeignKey('emocoes_detectadas.emocao_id'))
    distorcao_id = db.Column(db.Integer, db.ForeignKey('distorcao_cognitiva.distorcao_id'))
    questionamento_id = db.Column(db.Integer, db.ForeignKey('questionamento_socratico.questionamento_id'))

    usuario = db.relationship('Usuario', backref='conversas')
    emocao = db.relationship('EmocaoDetectada')
    distorcao = db.relationship('DistorcaoCognitiva')
    questionamento = db.relationship('QuestionamentoSocratico')

    @property
    def mensagem_usuario(self):
        try:
            return get_fernet().decrypt(self._mensagem_usuario.encode()).decode()
        except:
            return "[Erro ao ler mensagem]"

    @mensagem_usuario.setter
    def mensagem_usuario(self, value):
        try:
            self._mensagem_usuario = get_fernet().encrypt(value.encode()).decode()
        except:
            self._mensagem_usuario = "[Erro ao criptografar mensagem]"


class Emocao(db.Model):
    __tablename__ = 'emocoes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))

    def __repr__(self):
        return f'<Emocao {self.id} - {self.nome}>'


class Texto(db.Model):
    __tablename__ = 'texto'

    id = db.Column(db.Integer, primary_key=True)
    _conteudo = db.Column('conteudo', db.String(200))
    emocao_id = db.Column(db.Integer, db.ForeignKey('emocoes.id'))

    emocao = db.relationship('Emocao', backref='textos')

    def __repr__(self):
        return f'<Texto {self.id} - {self.conteudo}>'

    @property
    def conteudo(self):
        try:
            return get_fernet().decrypt(self._conteudo.encode()).decode()
        except:
            return "[Erro ao ler texto]"

    @conteudo.setter
    def conteudo(self, value):
        try:
            self._conteudo = get_fernet().encrypt(value.encode()).decode()
        except:
            self._conteudo = "[Erro ao criptografar texto]"


class Exercicio(db.Model):
    __tablename__ = 'exercicios'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=False)

    _texto = db.Column('texto', db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref='exercicios')

    @property
    def texto(self):
        try:
            return get_fernet().decrypt(self._texto.encode()).decode()
        except:
            return "[Erro ao ler exercício]"

    @texto.setter
    def texto(self, value):
        try:
            self._texto = get_fernet().encrypt(value.encode()).decode()
        except:
            self._texto = "[Erro ao criptografar exercício]"
