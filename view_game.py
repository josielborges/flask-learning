import time

from flask import render_template, request, redirect, session, flash, url_for, send_from_directory

from helpers import get_image, remove_image, GameForm
from main import app, db
from models import Game


@app.route('/')
def index():
    games_list = Game.query.order_by(Game.name)
    return render_template('gamelist.html', title='Games', games=games_list, session=session)


@app.route('/new')
def new_game():
    if 'logged_user' not in session:
        return redirect(url_for('login', next_page=url_for('new_game')))

    form = GameForm()

    return render_template('new_game.html', title='New Game', form=form)


@app.route('/edit/<int:id>')
def edit_game(id):
    if 'logged_user' not in session:
        return redirect(url_for('login', next_page=url_for('edit_game')))
    game = Game.query.filter_by(id=id).first()
    form = GameForm()
    form.name.data = game.name
    form.category.data = game.category
    form.console.data = game.console
    thumb = get_image(id)
    return render_template('edit_game.html', title='Edit Game', id=id, thumb=thumb, form=form)


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
    form_data = GameForm(request.form)

    if form_data.validate_on_submit():
        game = Game.query.filter_by(id=request.form['id']).first()
        game.name = form_data.name.data
        game.category = form_data.category.data
        game.console = form_data.console.data

        db.session.add(game)
        db.session.commit()

        file = request.files['file']
        if file != '':
            upload_path = app.config['UPLOAD_PATH']
            timestamp = time.time()
            remove_image(game.id)
            file.save(f'{upload_path}/thumb-{game.id}-{timestamp}.{file.filename.rsplit(".", 1)[1]}')

        return redirect(url_for('index'))

    print(form_data.errors)
    flash('Dados incorretos')


@app.route('/create', methods=['POST'])
def create_game():
    form_data = GameForm(request.form)

    if not form_data.validate_on_submit():
        print(form_data.errors)
        flash('Dados incorretos')
        return redirect(url_for('new_game'))

    name = form_data.name.data
    category = form_data.category.data
    console = form_data.console.data

    game = Game.query.filter_by(name=name).first()
    if game:
        flash('Game já existe')
        return redirect(url_for('index'))

    game = Game(name=name, category=category, console=console)
    db.session.add(game)
    db.session.commit()

    file = request.files['file']
    if file != '':
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        file.save(f'{upload_path}/thumb-{game.id}-{timestamp}.{file.filename.rsplit(".", 1)[1]}')

    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
