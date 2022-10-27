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
        movies_list = movie_service.get_all()

        director_id = request.args.get('director_id')
        if director_id is not None:
            movies_list = movie_service.get_by_director(director_id)

        genre_id = request.args.get('genre_id')
        if genre_id is not None:
            movies_list = movie_service.get_by_genre(genre_id)

        year = request.args.get('year')
        if year is not None:
            movies_list = movie_service.get_by_year(year)

        return movies_schema.dump(movies_list), 200

    def post(self):
        req_json = request.json
        try:
            movie = movie_service.create(req_json)
            return "", 201, {"location": f"/movies/{movie.id}"}
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
        movie = movie_service.get_one(mid)

        if movie is None:
            return {"error": "Movie not found"}, 404

        movie_service.delete_one(mid)

        return "", 204