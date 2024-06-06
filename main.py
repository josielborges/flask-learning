from flask import Flask, render_template, request, redirect, session, flash, url_for
from dotenv import load_dotenv
import os

load_dotenv()


class Game():
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console


game1 = Game(name='Resident Evil', category='Action', console='PS4')
game2 = Game(name='Metroid', category='RPG', console='Switch')
games_list = [game1, game2]

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


@app.route('/autenticate', methods=['POST'])
def autenticate():
    if 'alohomora' == request.form['password']:
        session['logged_user'] = request.form['user']
        flash(f'{session['logged_user']} logado com sucesso')
        next_page = request.form['next_page']
        print('11111111' + next_page)
        return redirect(next_page)
    else:
        flash(f'Usuário não encontrado')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('logged_user', None)
    flash(f'Logout efetuado com sucesso')
    return redirect(url_for('games'))


app.run(debug=True)
