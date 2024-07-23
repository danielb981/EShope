from django.shortcuts import render, redirect
from .models import New
from .filter import NewFilter
from costumerapp.models import Costumer

def news_list(request):
    news_queryset = New.objects.all()

    filter_object = NewFilter(
        data=request.GET,
        queryset=news_queryset
    )

    context = {"filter_object": filter_object}

    return render(request, 'news_list.html', context)

def new_detail(request, id): # id = 8
    # print(id) # 8
    one_new_object = New.objects.get(id=id)  # 1 объект

    one_new_object.views += 1  # меняем значение свойства объекта

    if request.user.is_authenticated:
        one_new_object.user_views.add(request.user)

    one_new_object.save()  # сохраняем в БД

    context = {"new": one_new_object}
    return render(request, 'news_detail.html', context)

def new_create(request):
    if request.method == "GET":
        return render(request, 'new_create.html')
    elif request.method == "POST":
        data = request.POST
        title = data["new_title"]
        text = data["new_article"]


        new_object = New.objects.create(
            title=title,
            article=text,
        )
        return redirect(f'/new-detail/{new_object.id}/')