from django.contrib.admin.models import LogEntry
from django.shortcuts import render

from logs.models import Logs


def activities_list(request):
    return render(request, 'logs/activities.html', context={"activities": Logs.objects.all()})


def my_logs(user_id, username, action_type, visited_url, description):
    log = Logs(user_id=user_id,
               username=username,
               action_type=action_type,
               visited_url=visited_url,
               description=description)
    log.save()


def logs(request):
    log = LogEntry.objects.all()
    return render(request, 'logs/logs.html', {'activity': log})
