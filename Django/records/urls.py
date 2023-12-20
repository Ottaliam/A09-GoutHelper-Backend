from django.urls import path

from . import views

urlpatterns = [
    path("record/addFoodRecord", views.addFoodRecord, name="add_food_record")
]