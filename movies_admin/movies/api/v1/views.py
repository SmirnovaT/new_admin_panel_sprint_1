from django.views.generic.list import BaseListView
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from movies.models import FilmWork


class MoviesMixinApi:
    model = FilmWork
    http_method_names = ["get"]
    paginate_by = 50

    def get_queryset(self):
        film_works = self.query()

        genres, actors, directors, writers = self.filter_persons()

        return film_works.annotate(
            genres=genres, actors=actors, directors=directors, writers=writers
        )

    def filter_persons(self):
        genres = ArrayAgg("genres__name", distinct=True)
        actors = ArrayAgg(
            "persons__full_name", distinct=True, filter=Q(personfilmwork__role="actor")
        )
        directors = ArrayAgg(
            "persons__full_name",
            distinct=True,
            filter=Q(personfilmwork__role="director"),
        )
        writers = ArrayAgg(
            "persons__full_name", distinct=True, filter=Q(personfilmwork__role="writer")
        )
        return genres, actors, directors, writers

    def query(self):
        film_works = FilmWork.objects.prefetch_related("genres").prefetch_related(
            "persons"
        )

        return film_works.values(
            "id", "title", "description", "creation_date", "rating", "type"
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesMixinApi, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )
        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }
        return context


class MoviesDetailApi(MoviesMixinApi, BaseDetailView):
    model = FilmWork
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {
            "results": [self.object],
        }
        return JsonResponse(context)

    def get_context_data(self, **kwargs):
        return self.object
