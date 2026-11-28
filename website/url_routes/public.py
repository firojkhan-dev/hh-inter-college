from django.urls import path

from website.views import (
    admission_enquiry,
    gallery_list,
    home,
    information_page,
    notice_detail,
    notice_list,
    site_search,
    switch_language,
    teacher_detail,
)


urlpatterns = [
    path("", home, name="home"),
    path("admission-enquiry/", admission_enquiry, name="admission_enquiry"),
    path("notices/", notice_list, name="notice_list"),
    path("notices/<int:pk>/", notice_detail, name="notice_detail"),
    path("gallery/", gallery_list, name="gallery_list"),
    path("teachers/<int:pk>/", teacher_detail, name="teacher_detail"),
    path("pages/<slug:slug>/", information_page, name="information_page"),
    path("search/", site_search, name="site_search"),
    path("language/", switch_language, name="switch_language"),
]
