from app.dao.models.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, gid):
        genre = self.session.query(Genre).get(gid)
        return genre

    def get_all(self):
        genres_list = self.session.query(Genre).all()
        return genres_list
