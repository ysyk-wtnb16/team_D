from . import views
from django.urls import path

app_name = 'travelp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('/search', views.SearchView.as_view(), name='search'),
]
