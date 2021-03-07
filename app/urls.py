from django.urls import path
from django.contrib import admin

from .api import api
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]
