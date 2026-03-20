from django.urls import path
from apps.todo.views import *


app_name = 'todo'

urlpatterns = [
    path('todos/', todo_list, name='list'),
    path('todos/<int:pk>/', todo_info, name='info'),
    path('todos/create/', create_todo, name='create'),
    path('todos/<int:pk>/update/', update_todo, name='update'),
    path('todos/<int:pk>/delete/', delete_todo, name='delete'),
]