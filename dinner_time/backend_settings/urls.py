"""backend_settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

SchemaView = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1.0',
        contact=openapi.Contact(email="zakharpetukhov@protonmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# Test sentry
def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('swagger/', SchemaView.with_ui('swagger'), name='swagger'),
    path('dinner/', include('apps.api.dinner.urls')),
    path('users/', include('apps.api.users.urls')),
    path('auth/', include('apps.api.authentication.urls')),
    path('company/', include('apps.api.company.urls')),
    path('settings/', include('apps.api.common.urls')),
    path('iiko/', include('apps.iiko.urls')),
    path('sentry-debug/', trigger_error),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
