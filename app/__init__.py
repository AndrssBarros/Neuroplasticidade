import os
import secrets
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager  
from dotenv import load_dotenv  

from app.ext import mail
from app.db_config import db
from app import models  

from app.auth.auth import auth_blueprint
from app.chatbot.routes_chatbot import chatbot_blueprint
from app.auth.controllers.configuracoes_controller import configuracoes
from app.auth.controllers.exercicio_controller import exercicio_bp
from app.chatbot.emocao_controller import emocao_blueprint

csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()  

def create_app():
    load_dotenv()  

    app = Flask(
        __name__,
        template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')),
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    )
    
    app.config['SECRET_KEY'] = '8f4a97a08c3e4a4f9a7c80a2c50a34d1edc6ef9130aa7bcfef6dfb72f690ac3f'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/dbsystemmatrix'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['FERNET_KEY'] = os.getenv('FERNET_KEY')   

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    app.register_blueprint(exercicio_bp)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(chatbot_blueprint, url_prefix='/chatbot')
    app.register_blueprint(configuracoes)
    app.register_blueprint(emocao_blueprint, url_prefix='/auth')  

    login_manager.init_app(app)   
    login_manager.login_view = 'auth.login'
    
    from app.models import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app
