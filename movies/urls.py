from django.urls import path
from .views import MovieListView, MovieDetailView, FavoriteCreateView

urlpatterns = [
    path('movies/', MovieListView.as_view()),
    path('movies/<int:pk>/', MovieDetailView.as_view()),
    path('favorites/', FavoriteCreateView.as_view()),
]