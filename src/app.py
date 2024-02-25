from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, setup_db, Movie, Actor

def create_app(test_config=None):

    # setup the app and the database
    app = Flask(__name__)
    app.app_context().push()
    if test_config is None:
        setup_db(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    # app routes

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE,PATCH"
        )
        return response

    @app.route("/actors", methods=["GET"])
    def get_actors():
        actors = Actor.query.order_by("name").all()
        if (len(actors) == 0):
            abort(404)
        formatted_actors = [actor.format() for actor in actors]
        db.session.close()
        return jsonify({
            "success": True,
            "actors": formatted_actors
        })

    @app.route("/movies", methods=["GET"])
    def get_movies():
        movies = Movie.query.order_by("title").all()
        if (len(movies) == 0):
            abort(404)
        formatted_movies = [movie.format() for movie in movies]
        db.session.close()
        return jsonify({
            "success": True,
            "movies": formatted_movies
        })
    
    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    def delete_actor(actor_id):
        error = False
        try:
            actor = db.session.get(Actor, actor_id)
            if actor is None:
                error = True
            actor.delete()
            updated_actors = Actor.query.order_by("name").all()
            updated_actors_formatted = [actor.format() for actor in updated_actors]
        except:
            abort(422)
        finally:
            if error:
                abort(404)
            else:
                return jsonify({
                    "success": True,
                    "deleted": actor_id,
                    "actors": updated_actors_formatted
                })
            
    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    def delete_movie(movie_id):
        error = False
        try:
            movie = db.session.get(Movie, movie_id)
            if movie is None:
                error = True
            movie.delete()
            updated_movies = Movie.query.order_by("title").all()
            updated_movies_formatted = [movie.format() for movie in updated_movies]
        except:
            abort(422)
        finally:
            if error:
                abort(404)
            else:
                return jsonify({
                    "success": True,
                    "deleted": movie_id,
                    "movies": updated_movies_formatted
                })
            
    @app.route("/actors", methods=["POST"])
    def create_actor():
        body = request.get_json()
        if body.get("name", None) is None:
            abort(400)
        try:
            actor = Actor(
                name = body.get("name", None),
                age = body.get("age", None),
                gender = body.get("gender", None),
                movies_id = body.get("movies_id", None)
            )
            actor.insert()

            updated_actors = Actor.query.order_by("name").all()
            updated_actors_formatted = [actor.format() for actor in updated_actors]
            return jsonify({
                "success": True,
                "created": actor.id,
                "actors": updated_actors_formatted
            })
        except:
            abort(422)

    @app.route("/movies", methods=["POST"])
    def create_movie():
        body = request.get_json()
        if body.get("title", None) is None:
            abort(400)
        try:
            movie = Movie(
                title = body.get("title", None),
                release_date = body.get("release_date", None),
                #actors = body.get("actors", None)
            )
            movie.insert()

            updated_movies = Movie.query.order_by("title").all()
            updated_movies_formatted = [movie.format() for movie in updated_movies]
            return jsonify({
                "success": True,
                "created": movie.id,
                "movies": updated_movies_formatted
            })
        except:
            abort(422)

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    def edit_actor(actor_id):
        error = False
        try:
            actor = db.session.get(Actor, actor_id)
            if actor is None:
                error = True
            body = request.get_json()
            name = body.get("name", None)
            age = body.get("age", None)
            gender = body.get("gender", None)
            movies_id = body.get("movies_id", None)
            if name:
                actor.name = name
            if age:
                actor.name = age
            if gender:
                actor.gender = gender
            if movies_id:
                actor.movies_id = movies_id
            actor.update()
        except:
            abort(422)
        finally:
            if error:
                abort(404)
            else:
                return jsonify({
                    "success": True,
                    "actor_id": actor.id
                })
            
    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    def edit_movie(movie_id):
        error = False
        try:
            movie = db.session.get(Movie, movie_id)
            if movie is None:
                error = True
            body = request.get_json()
            title = body.get("title", None)
            release_date = body.get("release_date", None)
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date
            movie.update()
        except:
            abort(422)
        finally:
            if error:
                abort(404)
            else:
                return jsonify({
                    "success": True,
                    "movie_id": movie.id
                })

    # Error handlers

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )
    
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal server error"})
        )
    
    return app
