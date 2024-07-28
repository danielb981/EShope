from .models import Costumer
from .forms import CostumerForm
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
def costumer_view(request):
    costumer_list = Costumer.objects.all()
    context = {"costumer_list": costumer_list}
    return render(request, 'costumers.html', context)

def costumer_create(request):
    if request.method == "POST":
        costumer_form = CostumerForm(request.POST)
        if costumer_form.is_valid():
            costumer_form.save()
            messages.success(request, "Покупатель добавлен!")
            return redirect('costumer-list')
    else:
        costumer_form = CostumerForm()
    return render(request, 'create_costumer.html', {'costumer_form': costumer_form})