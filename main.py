from flask import Flask, render_template, request, redirect


class Game():
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console


game1 = Game(name='Resident Evil', category='Action', console='PS4')
game2 = Game(name='Metroid', category='RPG', console='Switch')
games_list = [game1, game2]

app = Flask(__name__)


@app.route('/')
def games():
    return render_template('gamelist.html', title='Teste', games=games_list)


@app.route('/new')
def new_game():
    return render_template('new_game.html', title='New Game')


@app.route('/create', methods=['POST'])
def create_game():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']

    game = Game(name, category, console)
    games_list.append(game)

    return redirect('/')


app.run(debug=True)
