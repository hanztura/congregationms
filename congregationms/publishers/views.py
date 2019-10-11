#from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView

from .models import Publisher


# Create your views here.
class PublisherList(ListView):
    model = Publisher


class PublisherUpdate(UpdateView):
    model = Publisher
    fields = ['last_name', 'first_name', 'middle_name',
              'date_of_birth', 'date_of_baptism', 'contact_numbers']
    template_name = 'publishers/publisher_update.html'
    context_object_name = 'publisher'


class PublisherDetail(DetailView):
    model = Publisher
    context_object_name = 'publisher'
