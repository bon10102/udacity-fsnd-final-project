import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import datetime

from app import create_app
from models import db, setup_db, Movie, Actor
from settings import TEST_DB_NAME, DB_USER, DB_PASSWORD

class castingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)
        self.db = db
        self.new_actor = {
            "name": "test actor",
            "age": "20",
            "gender": "test",
            "movies_id": None
        }
        self.new_movie = {
            "title": "test movie",
            "release_date": datetime.date(2020, 1, 1),
        }
        
    def tearDown(self):
        self.db.session.close()
        pass

    def test_get_actors(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_get_actors_404(self):
        Actor.query.delete()
        res = self.client().get("/actors")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        self.db.session.rollback()

    def test_get_movies(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_get_movies_404(self):
        Actor.query.delete()
        Movie.query.delete()
        res = self.client().get("movies")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        self.db.session.rollback()

    def test_delete_actor(self):
        test_actor = Actor(
            name = "test actor",
            age = "20",
            gender = "test",
            movies_id = None
        )
        test_actor.insert()
        res = self.client().delete("/actors/" + str(test_actor.id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], test_actor.id)

    def test_delete_actor_404(self):
        res = self.client().delete("/actors/100000000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movie(self):
        test_movie = Movie(
            title = "test movie",
            release_date = datetime.date(2020, 1, 1),
        )
        test_movie.insert()
        res = self.client().delete("/movies/" + str(test_movie.id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], test_movie.id)

    def test_delete_movie_404(self):
        res = self.client().delete("/movies/100000000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_actor(self):
        res = self.client().post("/actors", json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["actors"]))
        created_actor = db.session.get(Actor, int(data["created"]))
        created_actor.delete()

    def test_create_actor_400(self):
        res = self.client().post("/actors", json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_create_movie(self):
        res = self.client().post("/movies", json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["movies"]))
        created_movie = db.session.get(Movie, data["created"])
        created_movie.delete()

    def test_create_movie_400(self):
        res = self.client().post("/movies", json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_edit_actor(self):
        test_actor = Actor(
            name = "test actor",
            age = "20",
            gender = "test",
            movies_id = None
        )
        test_actor.insert()
        res = self.client().patch("/actors/" + str(test_actor.id), json={"name": "test edited"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["actor_id"], test_actor.id)
        test_actor.delete()

    def test_edit_actor_404(self):
        res = self.client().patch("/actors/100000000000", json={"name": "test edited"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_edit_movie(self):
        test_movie = Movie(
            title = "test movie",
            release_date = datetime.date(2020, 1, 1),
        )
        test_movie.insert()
        res = self.client().patch("/movies/" + str(test_movie.id), json={"title": "test edited"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["movie_id"], test_movie.id)
        test_movie.delete()

    def test_edit_movie_404(self):
        res = self.client().patch("/movies/10000000000", json={"title": "test edited"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

# Make the tests available
if __name__ == "__main__":
    unittest.main()