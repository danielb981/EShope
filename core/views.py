from django.shortcuts import redirect, render, HttpResponse
from .models import *
from costumerapp.models import Costumer
from django.contrib.auth.models import User
from .forms import ProductForm, ProfileForm, UserForm, RegistrationForm, AuthForm
from .filters import ProductFilter
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def homepage(request):
    # SELECT * FROM Product;
    product_list = Product.objects.all()

    filter_object = ProductFilter(
        data=request.GET,
        queryset=product_list
    )

    context = {"filter_object": filter_object}
    # messages.add_message(request, messages.INFO, "Hello world")
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
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Товар добавлен успешно!")
            return redirect('/')
        else:
            messages.success(request, "Пройзошла ошибка!")
        return redirect('/')


def create_profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Профиль добавлен!")
            return redirect('profile_list')
        else:
            messages.success(request, "Пройзошла ошибка!")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'create_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def product_update(request, id):
    context = {}
    product_object = Product.object.get(id=id)
    context["form"] = ProductForm(instance=product_object)

    if request.method == "GET":
        return render(request, "product_update.html", context)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product_object)
        if form.is_valid():
            form.save()
            messages.success(request, "Товар изменен!")
            return redirect("/")
        return HttpResponse("Ошибка валидации!")

# def product_update(request, id):
#     product = get_object_or_404(Product, id=id)
#     if request.method == "POST":
#         form = ProductUpdateForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Товар успешно обновлен!")
#             return redirect('product-detail', id=product.id)
#         else:
#             messages.error(request, "Произошла ошибка при обновлении товара!")
#     else:
#         form = ProductUpdateForm(instance=product)
#     return render(request, 'product_update.html', {'form': form, 'product': product})

def profile_update(request, id):
    context = {}
    profile_object = Profile.objects.get(id=id)
    context["form"] = ProfileForm(instance=profile_object)

    if request.method == "GET":
        return render(request, "profile/update.html", context)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_object)
        if form.is_valid():
            form.save()
            return HttpResponse("Успешно обновлено!")
        return HttpResponse("Ошибка валидации!")


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
    # WHERE name LIKE '%keyword%' OR description LIKE '%keyword%'
    products = Product.objects.filter(
        Q(name__icontains=keyword) |
        Q(description__icontains=keyword) |
        Q(category__name__icontains=keyword)

    )
    context = {"products": products}
    return render(request, 'search_result.html', context)

def registration(request):
    context = {}

    if request.method == "POST":
        # create user object
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            user_object = reg_form.save()
            password = request.POST["password"]
            user_object.set_password(password)
            user_object.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('/')
        return HttpResponse("Ошибка валидации")

    reg_form = RegistrationForm()
    context["reg_form"] = reg_form
    return render(request, 'profile/registration.html', context)

def signin(request):
    context = {}

    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Вы успешно авторизовались!")
                return redirect('/')
        messages.warning(request, "Логин и/или пароль неверны")
    else:
        messages.warning(request, "Данные не валидны")

        form = AuthForm()
        context["form"] = form
        return render(request, 'profile/signin.html', context)



def signout(request):
    logout(request)
    return redirect('/')

