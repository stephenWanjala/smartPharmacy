from django.urls import path

from pharmacy import views

urlpatterns = [
    path("", views.loginPage, name="login")
]
