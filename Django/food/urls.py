from django.urls import path

from . import views

urlpatterns = [
    path("food/search", views.searchFood, name="search")
]