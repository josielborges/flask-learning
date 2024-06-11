from flask import render_template, request, redirect, session, flash, url_for
from flask_bcrypt import Bcrypt, check_password_hash

from helpers import UserForm
from main import app, db
from models import Appuser


@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    form = UserForm()
    return render_template('login.html', title='Login', next_page=next_page, form=form)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    form = UserForm(request.form)
    form_user = form.user.data
    next_page = request.form['next_page'] if request.form['next_page'] != 'None' else '/'
    user = Appuser.query.filter_by(username=form_user).first()

    valid_password = check_password_hash(user.password, form.password.data)

    if user and valid_password:
        session['logged_user'] = user.username
        flash(f'{user.name} logado com sucesso')
        return redirect(next_page)
    flash(f'Usuário não encontrado')
    return redirect(url_for('login', next_page=next_page))


@app.route('/logout')
def logout():
    session.pop('logged_user', None)
    flash(f'Logout efetuado com sucesso')
    return redirect(url_for('index'))


@app.route('/update_default_users_passwords')
def update_password():
    josiel = Appuser.query.filter_by(username='josiel').first()
    josiel.password = Bcrypt().generate_password_hash('1234').decode('utf-8')
    jussara = Appuser.query.filter_by(username='jussara').first()
    jussara.password = Bcrypt().generate_password_hash('5678').decode('utf-8')
    pedro = Appuser.query.filter_by(username='pedro').first()
    pedro.password = Bcrypt().generate_password_hash('4321').decode('utf-8')
    db.session.commit()
