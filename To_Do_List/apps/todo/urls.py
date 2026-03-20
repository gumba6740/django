from django.urls import path
from apps.todo.views import *
from apps.todo.cbvs import *


app_name = 'todo'

urlpatterns = [
    # FBV
    path('todos/', todo_list, name='list'),
    path('todos/<int:pk>/', todo_info, name='info'),
    path('todos/create/', create_todo, name='create'),
    path('todos/<int:pk>/update/', update_todo, name='update'),
    path('todos/<int:pk>/delete/', delete_todo, name='delete'),

    # CBV
    path('todos2/', ToDoListView.as_view(), name='cbv_list'),
]