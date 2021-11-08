from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

actors_movies = db.Table('actors_movies ',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
)
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    actors = db.relationship('Actor', secondary=actors_movies,
        backref=db.backref('table_many', lazy='dynamic'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    release_date = db.Column(db.DateTime )
    #lazy to add foto
    # first_foto_movie = db.Column(db.LargeBinary)


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)


class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name_short = db.Column(db.String(40), nullable=False)
    name_full = db.Column(db.String(100))


@app.route('/')
def hello():

    all_movies = Movie.query.all()
    return render_template('index.html',title="Main",
                           all_movies = all_movies )

@app.route('/genre_add', methods=['GET', 'POST'])
def genre_add():
   if request.method == "POST":
       # try: does not work correctly

        new_genre = Genre(name = request.form["genre_name"])
        db.session.add(new_genre)
        db.session.flush()
        new_movie = Movie(title = request.form["movie_title"],
                            genre_id = new_genre.id
                            )
        db.session.add(new_movie)
        db.session.commit()


       # except:
       #     db.session.rollback()
       #     print("Error add to DateBase")
   return render_template("genre_add.html", title="Добавить жанр")


if __name__== "__main__":
    app.run(debug=True)