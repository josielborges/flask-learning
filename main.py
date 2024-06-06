import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, flash, url_for

load_dotenv()


class Game():
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console


class User():
    def __init__(self, name, user, password):
        self.name = name
        self.user = user
        self.password = password


game1 = Game(name='Resident Evil', category='Action', console='PS4')
game2 = Game(name='Metroid', category='RPG', console='Switch')
games_list = [game1, game2]

user1 = User(name='Josiel', user='josiel', password='1234')
user2 = User(name='Jussara', user='jussara', password='5678')
user3 = User(name='Pedro', user='pedro', password='91011')

users = {
    user1.user: user1,
    user2.user: user2,
    user3.user: user3
}

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def games():
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

    game = Game(name, category, console)
    games_list.append(game)

    return redirect(url_for('games'))


@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    return render_template('login.html', title='Login', next_page=next_page)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    next_page = request.form['next_page'] if request.form['next_page'] is None else '/'
    form_user = request.form['user']
    if form_user in users:
        user = users[form_user]
        password = request.form['password']
        if user.password == password:
            session['logged_user'] = form_user
            flash(f'{session['logged_user']} logado com sucesso')
            return redirect(next_page)

    flash(f'Usuário não encontrado')
    return redirect(url_for('login', next_page=next_page))


@app.route('/logout')
def logout():
    session.pop('logged_user', None)
    flash(f'Logout efetuado com sucesso')
    return redirect(url_for('games'))


app.run(debug=True)
