from django.db.models.manager import BaseManager as BManager
from django.db.models.query import QuerySet


class BaseQuerySet(QuerySet):
    pass


class BaseManager(BManager):
    pass
