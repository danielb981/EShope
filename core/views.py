from django.shortcuts import redirect, render, HttpResponse
from .models import *
from costumerapp.models import Costumer
from django.contrib.auth.models import User
from .forms import ProductForm, ProfileForm, UserForm
from .filters import ProductFilter


# Create your views here.
def homepage(request):
    # SELECT * FROM Product;
    product_list = Product.objects.all()

    filter_object = ProductFilter(
        data=request.GET,
        queryset=product_list
    )

    context = {"filter_object": filter_object}

    # return HttpResponse("Hello Django!")
    return render(request, 'index.html', context)


def product_detail(request, id):
    # SELECT * FROM Product WHERE id = $id; -- где id - число с url
    product_object = Product.objects.get(id=id)

    # Увеличение просмотра
    product_object.views_qty += 1

    # Уникальные просмотры
    if request.user.is_authenticated:
        user = request.user
        if not Costumer.objects.filter(user=user).exists():
            costumer = Costumer.objects.create(
                name=user.username,
                age=0,
                gender='-',
                user=user,
            )
        costumer = user.costumer
        product_object.costumer_views.add(costumer)
        # product_object.costumer_views.add(request.user.costumer)

    # Сохранение в БД
    product_object.save()

    context = {
        "product": product_object,
    }
    return render(request, 'product_detail.html', context)

def product_create(request):
    context = {}
    context["product_form"] = ProductForm()

    if request.method == "GET":
        return render(request, 'product_create.html', context)
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            return HttpResponse("Успешно сохранено!")
        return HttpResponse("Ошибка валидации!")


def create_profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile_list')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'create_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def user_cabinet(request, id):
    user = User.objects.get(id=id)
    context = {"user": user}
    return render(request, 'cabinet.html', context)

def users_list(request):
    user_list = User.objects.all()
    context = {"users": user_list}
    return render(request, 'user.html', context)

def search(request):
    keyword = request.GET["keyword"]
    # LIKE
    products = Product.objects.filter(name__icontains=keyword)
    context = {"products": products}
    return render(request, 'search_result.html', context)

