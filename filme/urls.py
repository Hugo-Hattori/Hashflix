from django.urls import path, include
from .views import Homepage, Homefilmes

urlpatterns = [
    path('', Homepage.as_view()),
    path('filmes/', Homefilmes.as_view())
]