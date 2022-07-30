from project.config import config
from project.models import Genre, User, Director, Movie
from project.server import create_app, db

appl = create_app(config)


@appl.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "User": User,
        "Director": Director,
        "Movie": Movie
    }


if __name__ == '__main__':
    appl.run(
        host='localhost',
        port=25000,
        debug=True
    )
