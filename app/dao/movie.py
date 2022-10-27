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

    def get_by_director(self, director_id):
        movies_list = self.session.query(Movie).filter(Movie.director_id == director_id)
        return movies_list

    def get_by_genre(self, genre_id):
        movies_list = self.session.query(Movie).filter(Movie.genre_id == genre_id)
        return movies_list

    def get_by_year(self, year):
        movies_list = self.session.query(Movie).filter(Movie.year == year)
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