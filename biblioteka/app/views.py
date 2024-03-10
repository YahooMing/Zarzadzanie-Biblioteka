from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from .models import ToDoList, Item
from .forms import CreateNewList
from .models import Book
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'app/book_list.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'app/add_book.html', {'form': form})

def delete_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.delete()
    return redirect('book_list')

def toggle_availability(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.available = not book.available
    book.save()
    return redirect('book_list')

def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'app/edit_book.html', {'form': form})


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