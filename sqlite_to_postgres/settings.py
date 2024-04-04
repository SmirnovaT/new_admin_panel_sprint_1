import os
from dotenv import load_dotenv

from sqlite_to_postgres.models import (
    Genre,
    FilmWork,
    Person,
    PersonFilmWork,
    GenreFilmWork,
)

load_dotenv()

SQLITE_DB_PATH = os.environ.get("SQLITE_DB_PATH")
POSTGRES_DB_DSN = os.environ.get("POSTGRES_DB_DSN")
BUTCH_SIZE = int(os.environ.get("BUTCH_SIZE"))

mapping_table = {
    "genre": Genre,
    "film_work": FilmWork,
    "person": Person,
    "person_film_work": PersonFilmWork,
    "genre_film_work": GenreFilmWork,
}
