from django.urls import path
from vod0316.book.views import index, book, book_list, language


urlpatterns = [
    path('', index),
    path('book_list', book_list),
    path('book_list/<int:num>/', book),
    path('language/<str:lang>/', language),
]