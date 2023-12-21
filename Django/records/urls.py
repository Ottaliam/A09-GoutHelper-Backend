from django.urls import path

from . import views

urlpatterns = [
    path("record/addFoodRecord", views.addFoodRecord, name="add_food_record"),
    path("record/addUricacidRecord", views.addUricacidRecord, name="add_uricacid_record"),
    path("record/addFlareupRecord", views.addFlareupRecord, name="add_flareup_record"),

    path("record/chartFoodRecord", views.computeStatisticsAndChartsForFoodRecord, name="chart_food_record"),
]