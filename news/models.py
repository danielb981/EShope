from django.db import models
from django.contrib.auth.models import User


class NewsCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class New(models.Model):
    title = models.CharField(max_length=100)
    article = models.TextField(null=True,blank=True)
    category = models.ForeignKey(
        to=NewsCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Категория"
    )
    views = models.IntegerField(default=0)
    user_views = models.ManyToManyField(
        to=User,
        blank=True,
    )

    def __str__(self):
        return self.title