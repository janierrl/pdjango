from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import typing


class Search(models.Model):
    title: typing.Optional[str] = models.CharField(max_length=100, null=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    last_viewed_at: models.DateTimeField = models.DateTimeField(
        default=timezone.now)
    user: models.ForeignKey[User] = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title + " - by " + self.user.username
