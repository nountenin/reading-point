from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType
from book.models import *
from web_site_front.models import Slide

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(ReadPoint)
admin.site.register(Author)
admin.site.register(Rayon)
admin.site.register(Movement)
admin.site.register(Session)
admin.site.register(ContentType)
admin.site.register(Slide)

# Register your models here.
