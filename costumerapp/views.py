from django.shortcuts import render
from .models import Costumer

# Create your views here.
def costumer_view(request):
    costumer_list = Costumer.objects.all()
    context = {"costumer_list": costumer_list}
    return render(request, 'costumers.html', context)