from django.urls import path

from .views import (
    PublisherCreate, PublisherDelete, PublisherDetail,
    PublisherList, PublisherUpdate, GroupCreate, GroupDelete, GroupDetail, GroupList, GroupUpdate
)


app_name = 'publishers'
urlpatterns = [
    path('', PublisherList.as_view(), name='index'),
    path('groups/', GroupList.as_view(), name='group-index'),
    path('groups/new/', GroupCreate.as_view(), name='group-create'),
    path('groups/detail/<str:pk>/', GroupDetail.as_view(), name='group-detail'),
    path('groups/edit/<str:pk>/', GroupUpdate.as_view(), name='group-update'),
    path('groups/delete/<str:pk>/', GroupDelete.as_view(), name='group-delete'),
    path('edit/<str:pk>/', PublisherUpdate.as_view(), name='update'),
    path('detail/<str:pk>/', PublisherDetail.as_view(), name='detail'),
    path('new/', PublisherCreate.as_view(), name='create'),
    path('delete/<str:pk>/', PublisherDelete.as_view(), name='delete')
]
