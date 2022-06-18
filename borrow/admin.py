from django.contrib import admin
from borrow.models import Borrow, Parametre
from reader.models import Frequentation

admin.site.register(Borrow)
admin.site.register(Frequentation)
admin.site.register(Parametre)
# Register your models here.
