from django.urls import path

from .views import (
	MFSCreate, MFSDelete, MFSDetail, MFSList, MFSUpdate,
	MFSHistoryList
)

app_name = 'reports'
urlpatterns = [
    path('monthly-field-service/', MFSList.as_view(), name='mfs-index'),
    path('monthly-field-service/history/<str:publisher>/', MFSHistoryList.as_view(), name='mfs-history'),
    path('monthly-field-service/delete/<str:pk>/', MFSDelete.as_view(), name='mfs-delete'),
    path('monthly-field-service/new/', MFSCreate.as_view(), name='mfs-create'),
    path('monthly-field-service/<str:pk>/', MFSDetail.as_view(), name='mfs-detail'),
    path('monthly-field-service/update/<str:pk>/', MFSUpdate.as_view(), name='mfs-update')
]
