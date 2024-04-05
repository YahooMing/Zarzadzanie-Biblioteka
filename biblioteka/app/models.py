from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
    
class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('fantasy', 'Fantasy'),
        # Dodaj więcej gatunków według potrzeb
        ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    year = models.IntegerField()
    borrowed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book", null=True, blank=True)
    available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)
    publisher = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return self.title
    
    def is_available(self):
        return not self.borrowed_by
    
    def save(self, *args, **kwargs):
        if self.borrowed_by is not None:
            if(self.quantity > 0):
                self.quantity = 0
        else:
            self.quantity = 1
        if self.quantity == 0:
            self.available = False
        else:
            self.available = True
        super().save(*args, **kwargs)

#@receiver(post_save, sender=Book)
#def update_book_availability(sender, instance, created, **kwargs):
 #   if not created:  # Jeśli nie jest to nowo utworzony obiekt
  #      if instance.borrowed_by is not None:
   #         instance.available = False
    #        instance.save()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Wishlist: {self.book.title}"