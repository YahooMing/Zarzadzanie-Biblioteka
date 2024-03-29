# Generated by Django 5.0.2 on 2024-03-17 10:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_book_quantity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='borrowed_by',
        ),
        migrations.AddField(
            model_name='book',
            name='borrowed_by',
            field=models.ManyToManyField(blank=True, related_name='borrowed_books', to=settings.AUTH_USER_MODEL),
        ),
    ]
