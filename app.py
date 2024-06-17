from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
db = SQLAlchemy(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'clear' in request.form:
            db.session.query(Game).delete()
            db.session.commit()
            return redirect(url_for('index'))
        else:
            game_name = request.form['name']
            game_year = request.form['year']
            new_game = Game(name=game_name, year=game_year)
            db.session.add(new_game)
            db.session.commit()

    games = Game.query.all()
    return render_template('index.html', games=games)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
