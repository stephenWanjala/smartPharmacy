from django.urls import path

from pharmacy import views

urlpatterns = [
    path("", views.loginPage, name="login"),
    path('home', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    # path('sales', views.sales, name='sales'),
    path('categories', views.category, name='categories'),
    path('add_category', views.add_category, name='add_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
]
