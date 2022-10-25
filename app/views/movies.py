from flask import request
from flask_restx import Resource, Namespace

from app.container import movie_service
from app.dao.models.movie import MovieSchema

movie_ns = Namespace('movies')
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = movie_service.get_all()

        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        try:
            movie_service.create(req_json)
            return "", 201
        except Exception as e:
            return {"error": f"{e}"}, 400


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie = movie_service.get_one(mid)

        if movie is None:
            return {"error": "Movie not found"}, 404

        return movie_schema.dump(movie), 200

    def put(self, mid):
        req_json = request.json
        req_json['id'] = mid
        movie_service.update(req_json)

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
                return {"error": f"Поле {field} обязательно"}, 400

        return "", 204

    def delete(self, mid):
        movie_service.delete(mid)

        # if movie is None:
        #     return {"error": "Movie not found"}, 404

        return "", 204