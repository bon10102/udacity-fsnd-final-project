from flask_sqlalchemy import SQLAlchemy

from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_PATH_HOSTED

if DB_PATH_HOSTED != "":
    database_path = DB_PATH_HOSTED
else:
    database_path = "postgresql://{}:{}@{}/{}".format(
        DB_USER, DB_PASSWORD, "localhost:5432", DB_NAME
    )
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.close()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }

class Actor(db.Model):
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(75))
    movies = db.relationship("Movie", backref="Actor", cascade="all, delete-orphan", lazy=True)

    def __init__(self, name, age, gender, movies):
        self.name = name
        self.age = age
        self.gender = gender
        self.movies = movies

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.close()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "movies": self.movies
        }