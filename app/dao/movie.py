from app.dao.models.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        movie = self.session.query(Movie).get(mid)
        return movie

    def get_all(self):
        movies_list = self.session.query(Movie).all()
        return movies_list

    def create(self, data):
        movie = Movie(**data)

        self.session.add(movie)
        self.session.commit()

        return movie

    def update(self, movie):
        self.session.add(movie)
        self.session.commit()

        return movie

    def delete_one(self, mid):
        movie = self.get_one(mid)

        self.session.delete(movie)
        self.session.commit()