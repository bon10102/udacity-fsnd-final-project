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
        self.auth_header_cast_assist = {"authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtyOUNvTi1oYmNfbVVPRHdnbkM4cCJ9.eyJpc3MiOiJodHRwczovL2Rldi04cnR2eGxucjNxdHcwb3FpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NWI2OGU0M2ZkZjRhZTUyM2EwMDQ5NzgiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNzA4ODc1MjU5LCJleHAiOjE3MDg5NTk4NTksImF6cCI6ImUwMHVIZzkwMVNkTHBzNTNLVkJKVFhKWkt0UGdxdzBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.wBbn1hDnSuxMDXgAOrlxpJ6KsPZBCg_92zFujOCQsjmNdl-erKRDR2lLG0dqvjIEaPXIRSV0lYw7btU8uA1wgAADID4mEeVOmZQjLUbXsRdqva5SUizRp2UtRBTgL5jbKyDcAruHEBWfT6Ilq9a-aJjQM53-_ODjW9wPS4JgLf8Ky-J5YlGTgYi6ohM_tfywaYJsFgoRseIH9m9A_G8IMCCOesJx-mN96E0ADz4u9Bq1ifJ6s1NmbduaIqoQRCaMjzGcqiZRhNCeB4YZuglO4d6iuJ3zOu2vwFR2G8GqbPw6XlyvPz_ommyGoUIXYQ0s3kdUEkwdlhLnvDZpIJyj5w"}
        self.auth_header_cast_dir = {"authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtyOUNvTi1oYmNfbVVPRHdnbkM4cCJ9.eyJpc3MiOiJodHRwczovL2Rldi04cnR2eGxucjNxdHcwb3FpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NWJmZjVlOTY0ZTM0MmY2ZDZhZTBhNWEiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNzA4ODc4NDU0LCJleHAiOjE3MDg5NjMwNTQsImF6cCI6ImUwMHVIZzkwMVNkTHBzNTNLVkJKVFhKWkt0UGdxdzBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.TlzfV-fi9DnMmX3g_8JwKJ5ToTECnlxw_39DEBoe9gZWuGE0UvtFoO2LqaThtoDCUMfLNR1MThnAAZAT7Zw0QfVJDLi4zMNngI7ryiQyLH0N_F7X_aG2vSgarYmXsI2UEs6uMjTWq8207L5fDx8um8MaqHevl1H0rRZb5S2j4V9sGPhfWFHr187D9kJDqlxJtQV8inlyiHkuzKFepT1RsuLex5kXEBvCyjiC8Ue129_Lehf6uaZ9IyIfn7CBy3FTOHeTZWYs-kyzEQlCn2QrzrzfSlHbzGuFPwJrujAOWDB7MsmXKv9eEsQtC6GS49n5xG_bA0NddJS73QtzAd4A0w"}
        self.auth_exec_prod = {"authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtyOUNvTi1oYmNfbVVPRHdnbkM4cCJ9.eyJpc3MiOiJodHRwczovL2Rldi04cnR2eGxucjNxdHcwb3FpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NWRiNTlhMzM4ZGIwZGZjNGNjYTliYjQiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNzA4ODc4NTA5LCJleHAiOjE3MDg5NjMxMDksImF6cCI6ImUwMHVIZzkwMVNkTHBzNTNLVkJKVFhKWkt0UGdxdzBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.vXbww47y8hNqP6CmEzd9iMDdHcpqS33YeXcwpR1AAeLgoFmieRZi2FOS5CE2cLKWdO3alvEU6H515VBEizElqX5TNzq6fJPg5rcadJ2KFBfLtvsftwGQXUl4trUrOur1RHQBdvnZW43R4u4YfnbdEfmq15n4wPY-wkADFrQe_uoBAeaJi6ySGOu2039LO7YSPOy46F_2OHPWsLEpvtMdIcD_UIOlkZ4yGtoHWjXNtpYIVoMhC8Bf-p7FUA-A_nUBRFO9k8ddRUKuCivRi21DiLa9VXct4MVr9UiUFUK376yCNvZ-MyWcFXqBq21BQ4HooT4FiuqoR60S9y-c1V4B5w"}

    def tearDown(self):
        self.db.session.close()
        pass

    def test_get_actors(self):
        res = self.client().get(
            "/actors", 
            headers = self.auth_header_cast_assist
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_get_actors_404(self):
        Actor.query.delete()
        res = self.client().get(
            "/actors", 
            headers = self.auth_header_cast_assist
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        self.db.session.rollback()

    def test_get_movies(self):
        res = self.client().get(
            "/movies", 
            headers = self.auth_header_cast_assist
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_get_movies_404(self):
        Actor.query.delete()
        Movie.query.delete()
        res = self.client().get(
            "movies", 
            headers = self.auth_header_cast_assist
        )
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
        res = self.client().delete(
            "/actors/" + str(test_actor.id),
            headers = self.auth_header_cast_dir
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], test_actor.id)

    def test_delete_actor_404(self):
        res = self.client().delete(
            "/actors/100000000",
            headers = self.auth_header_cast_dir
        )
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
        res = self.client().delete(
            "/movies/" + str(test_movie.id),
            headers = self.auth_exec_prod
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], test_movie.id)

    def test_delete_movie_404(self):
        res = self.client().delete(
            "/movies/100000000",
            headers = self.auth_exec_prod
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_actor(self):
        res = self.client().post(
            "/actors", 
            json = self.new_actor,
            headers = self.auth_header_cast_dir
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["actors"]))
        created_actor = db.session.get(Actor, int(data["created"]))
        created_actor.delete()

    def test_create_actor_400(self):
        res = self.client().post(
            "/actors", 
            json = {},
            headers = self.auth_header_cast_dir
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_create_movie(self):
        res = self.client().post(
            "/movies", 
            json = self.new_movie,
            headers = self.auth_exec_prod
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["movies"]))
        created_movie = db.session.get(Movie, data["created"])
        created_movie.delete()

    def test_create_movie_400(self):
        res = self.client().post(
            "/movies", 
            json = {},
            headers = self.auth_exec_prod
        )
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
        res = self.client().patch(
            "/actors/" + str(test_actor.id), 
            json={"name": "test edited"},
            headers = self.auth_header_cast_dir
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["actor_id"], test_actor.id)
        test_actor.delete()

    def test_edit_actor_404(self):
        res = self.client().patch(
            "/actors/100000000000", 
            json={"name": "test edited"},
            headers = self.auth_header_cast_dir
        )
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
        res = self.client().patch(
            "/movies/" + str(test_movie.id), 
            json={"title": "test edited"},
            headers = self.auth_header_cast_dir
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["movie_id"], test_movie.id)
        test_movie.delete()

    def test_edit_movie_404(self):
        res = self.client().patch(
            "/movies/10000000000", 
            json = {"title": "test edited"},
            headers = self.auth_header_cast_dir
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

# Make the tests available
if __name__ == "__main__":
    unittest.main()