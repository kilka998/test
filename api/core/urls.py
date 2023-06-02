from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from core import settings

router = DefaultRouter()

api_v1_urls = [
    path('', include('company.urls')),
    path('', include(router.urls)),
]

admin_urls = [
    path('', admin.site.urls),
]

urlpatterns = [
    path('admin/', include(admin_urls)),
    path('api/v1/', include(api_v1_urls)),
]

if settings.DEBUG:
    docs_urls = [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
    urlpatterns.append(path('docs/', include(docs_urls)))

