from flask_restx import Resource, Namespace

from app.container import director_service
from app.dao.models.director import DirectorSchema

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = director_service.get_all()

        return directors_schema.dump(all_directors), 200


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        director = director_service.get_one(did)

        if director is None:
            return {"error": "Director not found"}, 404

        return director_schema.dump(director), 200
