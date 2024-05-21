from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path("home/", views.home, name="home"),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('books/<int:book_id>/toggle_availability/', views.toggle_availability, name='toggle_availability'),
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('books/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('mypage/', views.borrowed_books, name='borrowed_books'),
    path('mypage/<int:book_id>/', views.return_book, name='return_book'),
    path('add-to-wishlist/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('random_book/', views.random_book, name='random_book'),
    path('manage/', views.manage, name='manage'),
    path('confirm_taken/', views.confirm_taken, name='confirm_taken'),
    path('confirm_returned/', views.confirm_returned, name='confirm_returned'),
    path('add_opinion/<int:book_id>/', views.add_opinion, name='add_opinion'),
    path('delete_opinion/<int:opinion_id>/', views.delete_opinion, name='delete_opinion'),
    path('fetch-reviews/<int:book_id>/', views.fetch_reviews, name='fetch_reviews'),
    
]