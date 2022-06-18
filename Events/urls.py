from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers
from library_gn import settings
from . import views
from .views import GeneratePdf

route_event = routers.DefaultRouter()
route_event.register('event', views.viewapievent)

urlpatterns = [
    path('events', views.events, name='event'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('detail/<int:id>', views.detail_event, name='detail'),
    path('list_events/', views.list_events, name='list_events'),
    path('pdf/', GeneratePdf.as_view(), name='pdfprintEvents'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
