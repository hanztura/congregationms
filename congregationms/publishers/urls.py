from django.urls import path

from .views import PublisherDetail, PublisherList, PublisherUpdate


app_name = 'publishers'
urlpatterns = [
    path('', PublisherList.as_view(), name='index'),
    path('update/<str:pk>/', PublisherUpdate.as_view(), name='update'),
    path('detail/<str:pk>/', PublisherDetail.as_view(), name='detail')
]
