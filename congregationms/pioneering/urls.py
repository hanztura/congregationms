from django.urls import path

from .views import PioneerCreateView, PioneerDeleteView, PioneerDetailView, PioneerListView, PioneerUpdateView

app_name = 'pioneering'
urlpatterns = [
    path('detail/<slug:slug>/', PioneerDetailView.as_view(), name='detail'),
    path('new/', PioneerCreateView.as_view(), name='create'),
    path('edit/<slug:slug>/', PioneerUpdateView.as_view(), name='update'),
    path('delete/<str:pk>/', PioneerDeleteView.as_view(), name='delete'),
    path('', PioneerListView.as_view(), name='index'),
]