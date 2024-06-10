import time

from flask import render_template, request, redirect, session, flash, url_for, send_from_directory

from helpers import get_image, remove_image
from main import app, db
from models import Game, Appuser


@app.route('/')
def index():
    games_list = Game.query.order_by(Game.name)
    return render_template('gamelist.html', title='Games', games=games_list, session=session)


@app.route('/new')
def new_game():
    if 'logged_user' not in session:
        return redirect(url_for('login', next_page=url_for('new_game')))
    return render_template('new_game.html', title='New Game')


@app.route('/edit/<int:id>')
def edit_game(id):
    if 'logged_user' not in session:
        return redirect(url_for('login', next_page=url_for('edit_game')))
    game = Game.query.filter_by(id=id).first()
    thumb = get_image(id)
    return render_template('edit_game.html', title='Edit Game', game=game, thumb=thumb)


@app.route('/remove/<int:id>')
def remove_game(id):
    if 'logged_user' not in session:
        return redirect(url_for('login'))
    Game.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Game removed')
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update_game():
    game = Game.query.filter_by(id=request.form['id']).first()
    game.name = request.form['name']
    game.category = request.form['category']
    game.console = request.form['console']

    db.session.add(game)
    db.session.commit()

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    remove_image(game.id)
    file.save(f'{upload_path}/thumb-{game.id}-{timestamp}.{file.filename.rsplit(".", 1)[1]}')

    return redirect(url_for('index'))


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

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    file.save(f'{upload_path}/thumb-{game.id}-{timestamp}.{file.filename.rsplit(".", 1)[1]}')

    return redirect(url_for('index'))


@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    return render_template('login.html', title='Login', next_page=next_page)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    form_user = request.form['user']
    next_page = request.form['next_page'] if request.form['next_page'] != 'None' else '/'
    user = Appuser.query.filter_by(username=form_user).first()
    if user:
        password = request.form['password']
        if user.password == password:
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


@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
