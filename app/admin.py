from django.contrib import admin
from .models import Book, Wishlist, BooksToTake
# Register your models here.
admin.site.register(Book)
admin.site.register(Wishlist)
admin.site.register(BooksToTake)
