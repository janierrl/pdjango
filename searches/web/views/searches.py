from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ...models.search import Search
from ...models.result import Result
from ..forms.search_form import SearchForm
from ..utils.searching import search
from typing import Union
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages


@login_required
def searches(request):
    order_by_param = request.GET.get('order_by', '-created_at')

    if order_by_param in ['views_asc', 'views_desc']:
        order_field = '-last_viewed_at' if order_by_param == 'views_desc' else 'last_viewed_at'
        searches = Search.objects.filter(user=request.user).order_by(order_field)
    else:
        searches = Search.objects.filter(user=request.user).order_by(order_by_param)

    paginator = Paginator(searches, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not searches:
        messages.info(request, "No searches to display")

    return render(request, "searches/searches.html", {
        "page_obj": page_obj,
        "paginator": paginator,
        "order_by_param": order_by_param
    })


@login_required
def register_search(request: HttpRequest) -> Union[HttpResponse, HttpResponse]:
    if request.method == "POST":
        try:
            form = SearchForm(request.POST)
            new_search = form.save(commit=False)
            new_search.user = request.user

            language = form.cleaned_data.get("language")

            results = search(new_search.title, language)

            if results:
                new_search.save()

                for result_data in results:
                    new_result = Result(
                        title=result_data['title'],
                        preview=result_data['preview'],
                        url=result_data['url'],
                        search=new_search
                    )
                    new_result.save()

                return redirect("register_search")
            else:
                messages.error(
                    request, "No results were found for your query in the selected language")
        except ValueError:
            messages.error(request, "Please provide valid data")

    return render(request, "searches/register_search.html", {
        "form": SearchForm()
    })
