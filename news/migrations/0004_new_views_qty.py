# Generated by Django 5.0 on 2024-07-15 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_new_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='new',
            name='views_qty',
            field=models.IntegerField(default=0),
        ),
    ]