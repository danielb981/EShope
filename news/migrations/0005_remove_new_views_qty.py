# Generated by Django 5.0 on 2024-07-16 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_new_views_qty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new',
            name='views_qty',
        ),
    ]