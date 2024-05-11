from django import forms
from .models import Book,Wishlist


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'year','publisher', 'borrowed_by', 'available']

class AddToWishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = []

class GenreForm(forms.Form):
    genre_choices = Book.GENRE_CHOICES
    genre = forms.ChoiceField(choices=genre_choices)