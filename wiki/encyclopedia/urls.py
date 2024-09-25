from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("results", views.results, name="results"),
    path("createpage", views.create_page, name="createpage")
]


# Custom error handlers
handler404 = "encyclopedia.views.my_custom_page_not_found_view"
handler400 = "encyclopedia.views.my_custom_bad_request_view"