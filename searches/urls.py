from django.urls import path
from .web.views import home, authentication, searches, results

urlpatterns = [
    path("", home.home, name="home"),
    path("register/", authentication.signup, name="register"),
    path("login/", authentication.signin, name="login"),
    path("logout/", authentication.signout, name="logout"),
    path('manage_account/', authentication.manage_account, name='manage_account'),
    path('delete_account/', authentication.delete_account, name='delete_account'),
    path("searches/", searches.searches, name="searches"),
    path("searches/search/", searches.register_search, name="register_search"),
    path("searches/results/<int:id>/", results.results, name="results")
]