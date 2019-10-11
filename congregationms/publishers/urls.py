from django.urls import path

from .views import PublisherList


urlpatterns = [
    path('', PublisherList.as_view())
]
