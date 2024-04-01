from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from movies.mixin import UUIDMixin, TimeStampedMixin, CreatedTimeStampedMixin


class Genre(UUIDMixin, TimeStampedMixin):
    """Таблица "Жанры"."""

    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    """Таблица "Участники"."""

    full_name = models.CharField(_("full_name"), max_length=255, unique=True)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    """Таблица "Кинопроизведения"."""

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation_date"), blank=True, null=True)
    rating = models.FloatField(
        _("rating"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class TypeChoices(models.TextChoices):
        MOVIE = "movie", _("Movie")
        TV_SHOW = "tv_show", _("Show")

    type = models.CharField(
        _("type"),
        max_length=20,
        choices=TypeChoices.choices,
        default=TypeChoices.MOVIE,
    )
    file_path = models.FileField(
        _("file_path"), blank=True, null=True, upload_to="movies/"
    )
    genres = models.ManyToManyField(Genre, through="GenreFilmWork")
    persons = models.ManyToManyField(Person, through="PersonFilmWork")

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Film work")
        verbose_name_plural = _("Film works")
        indexes = [
            models.Index(fields=["creation_date", "rating"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin, CreatedTimeStampedMixin):
    """Таблица many-to-many, связывающая фильмы и жанры."""

    film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
    genre = models.ForeignKey(
        "Genre", verbose_name=_("Genre"), on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("film genre")
        verbose_name_plural = _("film genre")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "genre"],
                name="film_work_genre_idx",
            )
        ]


class PersonFilmWork(UUIDMixin, CreatedTimeStampedMixin):
    """Таблица many-to-many, связывающая фильмы и участников."""

    film_work = models.ForeignKey(
        "FilmWork", verbose_name=_("Film work"), on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        "Person", verbose_name=_("Participant"), on_delete=models.CASCADE
    )

    class RoleChoices(models.TextChoices):
        DIRECTOR = "director", _("Director")
        ACTOR = "actor", _("Actor")
        WRITER = "writer", _("Writer")

    role = models.CharField(_("role"), max_length=20, choices=RoleChoices.choices)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("Film participant")
        verbose_name_plural = _("Film participants")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"],
                name="film_work_person_role_unique_idx",
            )
        ]
