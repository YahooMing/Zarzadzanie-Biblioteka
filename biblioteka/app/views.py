from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import ToDoList, Item
from .forms import CreateNewList


def index(request, id):
    ls = ToDoList.objects.get(id=id)
    if ls in  request.user.todolist.all():
    #{"save":["save"],"c1":["clicked"]}
        if request.method == "POST":
            print(request.POST)
            if request.POST.get("save"):
                for item in ls.item_set.all():
                    if request.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif request.POST.get("newItem"):
                txt = request.POST.get("new")
                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid")

                
        return render(request, "app/list.html", {"ls": ls})
    else:
        return render(request, "app/view.html", {"ls": ls})


def home(request):
    return render(request, "app/home.html", {})

def create(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            request.user.todolist.add(t)
            return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(request, "app/create.html", {"form":form})

def view(request):
    return render(request, "app/view.html",{})