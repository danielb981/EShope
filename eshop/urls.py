"""
URL configuration for eshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import *
from costumerapp.views import *
from news.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('search/', search),
    path('product-create/', product_create, name='product-create'),
    path('product/<int:id>/', product_detail, name='product-detail'),
    path('costumers/', costumer_view, name='costumer-list'),
    path('costumer_create/', costumer_create, name='costumer-create'),
    path('profile/', create_profile, name='profile_list' ),
    path('profile_create/', create_profile, name='profile-create'),
    path('news/', news_list, name='news-list'),
    path('new-detail/<int:id>/', new_detail, name='new-detail'),
    path('new-create/', new_create, name='new-create'),
    path('users/', users_list),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)