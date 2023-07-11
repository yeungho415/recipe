"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('api/user/', include('user.urls')),
    path('api/recipe/', include('recipe.urls')),
]

# The SpectacularAPIView class in the drf_spectacular package is a Django
# class-based view, and it has a get method.

# The get method is invoked when a GET HTTP request is made to the URL
# associated with the SpectacularAPIView. When you browse to the api/schema/
# endpoint in a web browser, you're making a GET request, and so the get method
# of the SpectacularAPIView is called.

# This get method is responsible for generating and returning the OpenAPI schema
# for your API. It does this by examining your API's configuration, gathering metadata
# about its endpoints, and formatting this metadata according to the OpenAPI specification.

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

