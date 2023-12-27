from django.urls import path

from . import views

urlpatterns = [
    path("record/addFoodRecord", views.addFoodRecord, name="add_food_record"),
    path("record/addUricacidRecord", views.addUricacidRecord, name="add_uricacid_record"),
    path("record/addFlareupRecord", views.addFlareupRecord, name="add_flareup_record"),

    path("record/recordForDate", views.getFoodRecordsForDate, name="get_records_for_date"),
    
    path("record/foodRecordSummary", views.getFoodRecordSummary, name="food_record_summary"),
    path("record/uricRecordSummary", views.getUricacidSummary, name="uricacid_record_summary"),
    path("record/flareRecordSummary", views.getFlareupSummary, name="flareup_record_summary"),
]