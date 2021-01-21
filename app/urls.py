from api import views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'match', views.MatchViewSet)
router.register(r'ir', views.IrViewSet, base_name='ir_list')
router.register(r'v1/qltr', views.QueryViewSet)

schema_view = get_schema_view(title='Bookings API',
                description='An API to book matches or update odds.')

from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("ninja/", api.urls),  # <---------- !
    url(r'^api/indexing/solr/(?P<collection_name>[\w.@+-]+)$', include('django_solr_rest_apis.urls')),
    url(r'^$', include('django_dashboard_bs4.urls')),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title='Bookings API'))
]
urlpatterns += router.urls
