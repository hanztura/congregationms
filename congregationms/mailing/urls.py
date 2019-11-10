from django.urls import path

from .views import MailCreateView

app_name = 'mailing'
urlpatterns = [
    path('new/<str:publisher>', MailCreateView.as_view(), name='new'),
]
