from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from .models import Book
from .forms import BookForm
from django.contrib.auth.decorators import login_required

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

#@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.available:
        book.borrowed_by = request.user
        book.save()
            #return redirect('book_detail', book_id=book.id)  # Przekierowanie na stronę szczegółów książki
    return redirect('book_list')

#@login_required
def borrowed_books(request):
    user_borrowed_books = Book.objects.filter(borrowed_by=request.user)
    return render(request, 'app/mypage.html', {'borrowed_books': user_borrowed_books})

def return_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.borrowed_by == request.user:
        book.borrowed_by = None
        book.save()
            #return redirect('book_detail', book_id=book.id)
    return redirect('borrowed_books')

def home(request):
    return render(request, "app/home.html", {})

