from functools import wraps
from flask import session,flash,redirect,url_for

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        else:
            flash('You need to login first.', 'is-error')
            return redirect(url_for('auth.login'))

    return wrap