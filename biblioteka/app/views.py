from django.http import HttpResponse
from django.shortcuts import render
from .models import ToDoList, Item


def index(request, name):
    ls = ToDoList.objects.get(name=name)
    items = ls.item_set.get(id=1)
    return render(request, "app/list.html", {"ls": ls})

def home(request):
    return render(request, "app/home.html", {})