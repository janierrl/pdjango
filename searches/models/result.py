from django.db import models
from .search import Search
import typing


class Result(models.Model):
    title: typing.Optional[str] = models.CharField(max_length=255, null=True)
    preview: typing.Optional[str] = models.TextField(null=True)
    url: typing.Optional[str] = models.CharField(max_length=200, null=True)
    search: models.ForeignKey[Search] = models.ForeignKey(
        Search, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title + " - by " + self.search.title
