from django.urls import path

from .views import dashboard, AccountView

app_name = 'system'
urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('account/', AccountView.as_view(), name='account'),
]
