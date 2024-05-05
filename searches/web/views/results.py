from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ...models.search import Search
from ...models.result import Result
from django.http import HttpRequest, HttpResponse, Http404
from django.utils import timezone


@login_required
def results(request: HttpRequest, id: int) -> HttpResponse:
    try:
        search = Search.objects.get(pk=id, user=request.user)
    except Search.DoesNotExist:
        raise Http404("Search not found or does not belong to this user")

    results = Result.objects.filter(search=search)
    search.last_viewed_at = timezone.now()
    search.save()

    return render(request, "results/results.html", {
        "results": results,
        "search": search
    })
