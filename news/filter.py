from .models import New
import django_filters


class NewFilter(django_filters.FilterSet):
    class Meta:
        model = New
        fields = ['title', 'article', 'category']