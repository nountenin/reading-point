from django.contrib import admin
from django.contrib.admin.models import LogEntry

from logs.models import Logs

admin.site.register(Logs)
admin.site.register(LogEntry)
