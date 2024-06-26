from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from .models import Book, Wishlist, BooksToTake, LocalOpinions
from .forms import BookForm,AddToWishlistForm,GenreForm
from django.contrib.auth.decorators import login_required
import random
from datetime import datetime
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .scraper import fetch_external_reviews
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import requests

@login_required
def book_list(request):
    query = request.GET.get('search_query')
    
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query) | Book.objects.filter(genre__icontains=query)
    else:
        books = Book.objects.all()

    for book in books:
        book.user_has_opinion = book.localopinions_set.filter(user=request.user).exists()


    user = request.user
    return render(request, 'app/book_list.html', {'books': books, 'user': user})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'app/add_book.html', {'form': form})

@login_required
def delete_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.delete()
    return redirect('book_list')

@login_required
def toggle_availability(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.available = not book.available
    book.save()
    return redirect('book_list')

@login_required
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

@login_required
def borrow_book(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(pk=book_id)
        if book.available:
            location = request.POST.get('location')
            date_str = request.POST.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Konwersja daty z formatu tekstowego
            
            # Usuń wszystkie istniejące rekordy związane z tą książką w modelu BooksToTake
            BooksToTake.objects.filter(book=book).delete()

            # Stwórz nowy rekord w modelu BooksToTake
            with transaction.atomic():
                book.borrowed_by = request.user
                book.save()
                BooksToTake.objects.create(user=request.user, book=book, location=location, date=date)
                messages.success(request, f'Book "{book.title}" borrowed successfully!')
        else:
            messages.error(request, f'Book "{book.title}" is not available for borrowing!')
        return redirect('book_list')


@login_required
def borrowed_books(request):
    user_borrowed_books = Book.objects.filter(borrowed_by=request.user)
    books_to_take = BooksToTake.objects.filter(user=request.user)
    return render(request, 'app/mypage.html', {'borrowed_books': user_borrowed_books, 'books_to_take': books_to_take})

@login_required
def return_book(request, book_id):
    book=BooksToTake.objects.get(book=book_id)
    book.requested_to_return = True
    book.save()
    return redirect('borrowed_books')

def home(request):
    return render(request, "app/home.html", {})

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
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

@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = Wishlist.objects.get(id=wishlist_id)
    wishlist_item.delete()
    return redirect('wishlist')

@login_required
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

@login_required
def manage(request):
    all_borrowed_books = BooksToTake.objects.all()
    return render(request, 'app/manage.html', {'all_borrowed_books': all_borrowed_books})

@login_required
def confirm_taken(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = BooksToTake.objects.get(pk=book_id)
        book.is_taken = True
        book.save()
        return redirect('manage')
    
@login_required
def confirm_returned(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = BooksToTake.objects.get(pk=book_id)
        book.is_taken = False
        book.is_returned = True
        book.save()
        book_details = Book.objects.get(pk=book.book.id)
        book_details.borrowed_by = None
        book_details.save()
        book.delete()
        return redirect('manage')
    
@login_required
def add_opinion(request, book_id):
    book = Book.objects.get(pk=book_id)
    user_opinion = LocalOpinions.objects.filter(book=book, user=request.user).exists()
    if request.method == 'POST':
        if not user_opinion:  # Sprawdzanie, czy użytkownik już wystawił opinię
            opinion_text = request.POST.get('opinion')
            rating = request.POST.get('rating')
            LocalOpinions.objects.create(book=book, user=request.user, opinion=opinion_text, rating=rating, read=True)
    return redirect('book_list')
    

def delete_opinion(request, opinion_id):
    opinion = get_object_or_404(LocalOpinions, pk=opinion_id)
    
    # Sprawdź, czy żądający użytkownik jest właścicielem opinii
    if opinion.user == request.user:
        opinion.delete()
    
    return redirect('book_list')  # Przekieruj użytkownika na stronę z listą książek


@login_required
def fetch_reviews(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    external_reviews = fetch_external_reviews(book.title)
    if not external_reviews:
        external_reviews = ["No reviews found."]
    return JsonResponse({'reviews': external_reviews})


@login_required
def home(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    for item in wishlist_items:
        if item.book.available:
            messages.info(request, f'Book "{item.book.title}" from your wishlist is now available!')

    return render(request, "app/home.html", {})