import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Game %r>' % self.name


class Appuser(db.Model):
    username = db.Column(db.String(8), primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Game %r>' % self.name


@app.route('/')
def index():
    games_list = Game.query.order_by(Game.name)
    return render_template('gamelist.html', title='Games', games=games_list)


@app.route('/new')
def new_game():
    if 'logged_user' not in session:
        return redirect(url_for('login', next_page=url_for('new_game')))
    return render_template('new_game.html', title='New Game')


@app.route('/create', methods=['POST'])
def create_game():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']

    game = Game.query.filter_by(name=name).first()
    if game:
        flash('Game já existe')
        return redirect(url_for('index'))

    game = Game(name=name, category=category, console=console)
    db.session.add(game)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    return render_template('login.html', title='Login', next_page=next_page)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    form_user = request.form['user']
    next_page = request.form['next_page'] if request.form['next_page'] is not None else '/'
    user = Appuser.query.filter_by(username=form_user).first()
    if user:
        password = request.form['password']
        if user.password == password:
            session['logged_user'] = user.nickname
            flash(f'{user.name} logado com sucesso')
            return redirect(next_page)
    flash(f'Usuário não encontrado')
    return redirect(url_for('login', next_page=next_page))


@app.route('/logout')
def logout():
    session.pop('logged_user', None)
    flash(f'Logout efetuado com sucesso')
    return redirect(url_for('index'))


app.run(debug=True)
