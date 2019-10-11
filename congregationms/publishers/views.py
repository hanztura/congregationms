from django.shortcuts import render
from django.views.generic import ListView

from .models import Publisher


# Create your views here.
class PublisherList(ListView):
    model = Publisher
