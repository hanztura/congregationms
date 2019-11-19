from django.urls import path

from .views import ServantCreateView, ServantDetailView, ServantUpdateView, ServantListView


app_name = 'servants'
urlpatterns = [
    path('', ServantListView.as_view(), name='index'),
    path('new/', ServantCreateView.as_view(), name='create'),
    path('delete/<str:pk>/', ServantDetailView.as_view(), name='delete'),
    path('detail/<str:pk>/', ServantDetailView.as_view(), name='detail'),
    path('update/<str:pk>/', ServantUpdateView.as_view(), name='update'),
]
