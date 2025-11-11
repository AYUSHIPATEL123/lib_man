from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('books/',views.books, name='books'),
    path('book_details/<slug:book_slug>/', views.book_details, name='book_detail'),
    path('request_book/<slug:book_slug>/', views.request_book, name='issue_details'),
    path('user_books/', views.user_books, name='user_books'),
    path('update_status/<int:id>/', views.update_status, name='update_status'),
    path('add_books/', views.add_books, name='add_book'),
    path('dashboard/', views.dashboard, name='dashboard'),
]