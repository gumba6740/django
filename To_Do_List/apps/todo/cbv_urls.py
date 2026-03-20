from django.urls import path
from apps.todo.cbvs import *


app_name = 'cbv_todo'

urlpatterns = [
    path('todos2/', ToDoListView.as_view(), name='list'),
]
