from flask import Blueprint
from app.auth.controllers import auth_controller, static_controller
from app.chatbot import emocao_controller


auth_blueprint = Blueprint('auth', __name__)

auth_blueprint.add_url_rule('/inicio', view_func=static_controller.inicio, methods=['GET', 'POST'])
auth_blueprint.add_url_rule('/distorcoes', view_func=static_controller.distorcoes, methods=['GET', 'POST'])
auth_blueprint.add_url_rule('/exercicios', view_func=static_controller.exercicios, methods=['GET', 'POST'])
auth_blueprint.add_url_rule('/dados', view_func=static_controller.dados, methods=['GET'])

auth_blueprint.add_url_rule('/cadastro', view_func=auth_controller.cadastro, methods=['GET', 'POST'])
auth_blueprint.add_url_rule('/login', view_func=auth_controller.login, methods=['GET', 'POST'])
auth_blueprint.add_url_rule('/logado', view_func=auth_controller.logado, methods=['GET', 'POST'])
auth_blueprint.add_url_rule('/solicitar-redefinicao', view_func=auth_controller.solicitar_redefinicao, methods=['GET', 'POST'])
auth_blueprint.add_url_rule('/resetar-senha/<token>', view_func=auth_controller.redefinir_senha, methods=['GET', 'POST'])

auth_blueprint.add_url_rule('/emocoes', view_func=emocao_controller.registro_emocoes, methods=['GET'])
