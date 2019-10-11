from django.urls import path

from .views import MFSDetail, MFSList

app_name = 'reports'
urlpatterns = [
    path('monthly-field-service/', MFSList.as_view(), name='mfs-index'),
    path('monthly-field-service/<str:pk>/', MFSDetail.as_view(), name='mfs-detail')
]
