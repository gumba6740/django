from django.urls import path
from apps.todo.cbvs import *


app_name = 'cbv_todo'

urlpatterns = [
    path('todos2/', ToDoListView.as_view(), name='list'),
    path('todos2/<int:pk>', TodoDetailView.as_view(), name='info'),
]
