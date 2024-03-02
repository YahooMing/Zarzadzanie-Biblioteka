from django.http import HttpResponse
from django.shortcuts import render
from .models import ToDoList, Item


def index(request, name):
    ls = ToDoList.objects.get(name=name)
    items = ls.item_set.get(id=1)
    return HttpResponse("%s <br> %s" % (ls.name,str(items.text)))

def home(request):
    return render(request, "app/base.html", {"name":"Szymon"})