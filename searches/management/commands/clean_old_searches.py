from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ..utils.cleanup import clean_old_searches


class Command(BaseCommand):
    help = 'Cleans old searches for all users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            clean_old_searches(user)
