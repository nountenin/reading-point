from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework import routers

from web_site_front.views import HomeSite as home
from Events.urls import route_event
from formulairmail.views import vuemail, email
from book import views
from django.conf import settings
from django.conf.urls.static import static
from siteweb.urls import router as contact_api
from book.urls import router as route_book, router_read_point, Category_router
from statistiques.views import reader_statistics
route = routers.DefaultRouter()
route.registry.extend(route_book.registry)
route.registry.extend(router_read_point.registry)
route.registry.extend(contact_api.registry)
route.registry.extend(route_event.registry)
route.registry.extend(Category_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls,name="admin"),
    path("books/", include('book.urls')),
    path("readers/", include('reader.urls')),
    path("subscription/", include('subscription.urls')),
    path("borrow/", include('borrow.urls')),
    path("dashboard", reader_statistics, name="dashboard"),
    path("", home, name='home_site'),
    path("accounting/", include('accounting.urls')),
    # path("users/", views.dashboard, name="users"),
    path("stat/", views.dashboard, name="stat"),
    path('mail/', email, name="mail"),
    path('api/', include(route.urls)),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('statistic/', include('statistiques.urls')),
    path('siteweb/', include('siteweb.urls')),
    path('logs/', include('logs.urls')),
    path("Events/", include('Events.urls')),
    path("web_site_front/", include('web_site_front.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
