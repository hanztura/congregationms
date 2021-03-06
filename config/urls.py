"""congregationms URL Configuration

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
from django.urls import include, path

from debug_toolbar import urls as debug_toolbar_urls
from rest_framework import routers

from cities.api.viewsets import CityViewSet, CountryViewSet, StateViewSet
from publishers.api.viewsets import GroupViewSet
from reports.api.viewsets import MFSViewSet
from system.views import home, login, logout

router = routers.DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'states', StateViewSet)
router.register(r'cities', CityViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'mfs', MFSViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    path('accounts/', include('django.contrib.auth.urls')),
    path('mailing/', include('mailing.urls')),
    path('pioneering/', include('pioneering.urls')),
    path('publishers/', include('publishers.urls')),
    path('reports/', include('reports.urls')),
    path('servants/', include('servants.urls')),
    path('login/', login, name='system-login'),
    path('logout/', logout, name='system-logout'),
    path('', include('system.urls')),
    path('', home, name='home'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar_urls))
    ]
