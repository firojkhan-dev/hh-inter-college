from django.urls import include, path

from website.url_routes import public, staff


urlpatterns = [
    path("", include(public.urlpatterns)),
    path("", include(staff.urlpatterns)),
]
