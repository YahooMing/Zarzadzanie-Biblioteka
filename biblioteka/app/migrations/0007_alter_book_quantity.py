# Generated by Django 5.0.2 on 2024-03-15 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_todolist_user_delete_item_delete_todolist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]