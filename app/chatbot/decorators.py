import uuid
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper

def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']