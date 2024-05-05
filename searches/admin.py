from django.contrib import admin
from .models.search import Search
from .models.result import Result


admin.site.register(Search)
admin.site.register(Result)
