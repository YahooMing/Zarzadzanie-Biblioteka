from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path("<int:id>",views.index, name="index"),
    path("home/", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("home/", views.home, name="home"),
    path("view/", views.view, name="view"),
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
]