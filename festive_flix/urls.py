from django.urls import path

from . import views

urlpatterns = [
    path("", views.search_holiday_movies, name="holiday_movies"),
]