from app import models, db, schemas
from flask import current_app as app, request, jsonify
from flask_restx import Api, Resource

from app.models import Movie, Director, Genre
from app.schemas import MovieSchema, DirectorSchema, GenreSchema

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = Movie.query.all()

        director_id = request.args.get('director_id')
        if director_id:
            all_movies = Movie.query.filter(Movie.director_id == director_id)

        genre_id = request.args.get('director_id')
        if genre_id:
            all_movies = Movie.query.filter(Movie.genre_id == genre_id)

        if director_id and genre_id:
            all_movies = Movie.query.filter((Movie.director_id == director_id) & (Movie.genre_id == genre_id))

        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        try:
            new_movie = Movie(**req_json)
            with db.session.begin():
                db.session.add(new_movie)
            return '', 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        return movie_schema.dump(movie), 200

    def put(self, mid):
        req_json = request.json
        movie = Movie.query.get(mid)

        required_fields = [
                'title',
                'description',
                'trailer',
                'year',
                'rating',
                'genre_id',
                'director_id'
            ]

        for field in required_fields:
            if field not in req_json:
                return f'Поле {field} обязательно', 400

        movie.title = req_json.get('title')
        movie.description = req_json.get('description')
        movie.trailer = req_json.get('trailer')
        movie.year = req_json.get('year')
        movie.rating = req_json.get('rating')
        movie.genre_id = req_json.get('genre_id')
        movie.director_id = req_json.get('director_id')

        db.session.add(movie)
        db.session.commit()

        return '', 204

    def delete(self, mid):
        try:
            movie = Movie.query.get(mid)
            db.session.delete(movie)
            db.session.commit()

            return '', 204

        except Exception as e:
            print(e)
            db.session.rollback()

            return e, 200


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = Director.query.all()

        return directors_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        try:
            new_director = Director(**req_json)
            with db.session.begin():
                db.session.add(new_director)

            return '', 201

        except Exception as e:
            print(e)
            db.session.rollback()

            return e, 200



@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        director = Director.query.get(did)

        return director_schema.dump(director), 200

    def put(self, did):
        req_json = request.json
        director = Director.query.get(did)

        required_fields = [
            'name'
        ]

        for field in required_fields:
            if field not in req_json:
                return f'Поле {field} обязательно', 400

        director.name = req_json.get('name')

        db.session.add(director)
        db.session.commit()

        return '', 204

    def delete(self, did):
        try:
            director = Director.query.get(did)
            db.session.delete(director)
            db.session.commit()

            return '', 204

        except Exception as e:
            print(e)
            db.session.rollback()

            return e, 200


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = Genre.query.all()

        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        try:
            new_genre = Genre(**req_json)
            with db.session.begin():
                db.session.add(new_genre)

            return '', 201

        except Exception as e:
            print(e)
            db.session.rollback()

            return e, 200


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        genre = Genre.query.get(gid)

        return genre_schema.dump(genre), 200

    def put(self, gid):
        req_json = request.json
        genre = Genre.query.get(gid)

        required_fields = [
            'name'
        ]

        for field in required_fields:
            if field not in req_json:
                return f'Поле {field} обязательно', 400

        genre.name = req_json.get('name')

        db.session.add(genre)
        db.session.commit()

        return '', 204

    def delete(self, gid):
        try:
            genre = Genre.query.get(gid)
            db.session.delete(genre)
            db.session.commit()

            return '', 204

        except Exception as e:
            print(e)
            db.session.rollback()

            return e, 200
