from django.urls import path
from logs.views import activities_list, logs

urlpatterns = [
    path('activities/', activities_list, name="activities"),
    path('action/',logs, name="logs")
]
