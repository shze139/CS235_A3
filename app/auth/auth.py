from flask import Blueprint,request,render_template,session,flash,redirect,url_for
from app.utilities.forms import LoginForm,RegisterForm
from app.adapters.repository import repo_instance as repo
import app.auth.services as services

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET','POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        try:
            user = services.login(username, password, repo)
            session['username'] = username
            session['userId'] = user.id
            return redirect(url_for('home.index'))
        except services.LoginFailedException:
            flash('Username or password is error', 'is-error')

    return render_template('login.html', form=form)

@bp.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        try:
           services.register(username, password, repo)
           flash('Register successful.', 'is-success')
           return redirect(url_for('auth.login'))
        except services.UsernameNotUniqueException:
            flash('Username has been used.', 'is-error')

    return render_template('register.html', form=form)

@bp.route('/logout', methods=('GET',))
def logout():
    session.clear()
    return redirect(url_for('home.index'))

