from django.utils import timezone
from ...models.search import Search


def clean_old_searches(user):
    deadline = timezone.now() - timezone.timedelta(hours=24)
    old_searches = Search.objects.filter(user=user, created_at__lt=deadline).order_by('created_at')[:10]
    old_searches.delete()