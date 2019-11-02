from django.urls import path

from .views import dashboard

app_name = 'system'
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard')
]