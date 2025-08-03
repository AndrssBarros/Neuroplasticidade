import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter
from markupsafe import Markup
from sqlalchemy.orm import joinedload
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask import render_template
from app.roda import gerar_roda_emocoes
from app.db_config import db
from app.chatbot.forms import LoginForm, RegistrationForm
from app.db_config import db
