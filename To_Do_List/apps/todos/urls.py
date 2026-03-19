from django.urls import path
from apps.todos.views import *


app_name = 'todos'

urlpatterns = [
    path('todos/', todo_list, name='todo_list'),
    path('todos/<int:pk>/', todo_info, name='todo_info'),
    path('todos/create/', create_todo, name='create_todo'),
    path('todos/<int:pk>/update/', update_todo, name='update_todo'),
]