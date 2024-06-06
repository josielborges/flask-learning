from flask import Flask, render_template

app = Flask(__name__)


class Game():
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console


@app.route('/')
def main():
    game1 = Game(name='Resident Evil', category='Action', console='PS4')
    game2 = Game(name='Metroid', category='RPG', console='Switch')

    games = [game1, game2]
    return render_template('gamelist.html', title='Teste', games=games)


@app.route('/new')
def new_game():
    return render_template('new_game.html', title='New Game')


app.run()
