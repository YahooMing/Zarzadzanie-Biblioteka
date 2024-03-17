from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book

#@receiver(post_save, sender=Book)
#@receiver(post_delete, sender=Book)
#def update_book_availability(sender, instance, **kwargs):
#    if instance.borrowed_by:
#        instance.available = False
#    else:
#        instance.available = True
#    instance.save()