from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from .models import Book, Wishlist
from .forms import BookForm,AddToWishlistForm,GenreForm
from django.contrib.auth.decorators import login_required
import random

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

def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items})

def add_to_wishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = AddToWishlistForm(request.POST)
        if form.is_valid():
            wishlist_item = form.save(commit=False)
            wishlist_item.user = request.user
            wishlist_item.book = book
            wishlist_item.save()
            return redirect('wishlist')
    else:
        form = AddToWishlistForm()
    return render(request, 'add_to_wishlist.html', {'form': form, 'book': book})

def remove_from_wishlist(request, wishlist_id):
    wishlist_item = Wishlist.objects.get(id=wishlist_id)
    wishlist_item.delete()
    return redirect('wishlist')

def random_book(request):
    error_message = None
    random_book = None

    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            selected_genre = form.cleaned_data['genre']
            books = Book.objects.filter(genre=selected_genre)
            if books.exists():
                random_book = random.choice(books)
            else:
                error_message = 'There are no books available for the selected genre.'
    else:
        form = GenreForm()

    return render(request, 'app/random_book.html', {'form': form, 'random_book': random_book, 'error_message': error_message})