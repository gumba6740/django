from django.urls import path
from apps.todo.cbvs import *


app_name = 'cbv_todo'

urlpatterns = [
    path('todos/', ToDoListView.as_view(), name='list'),
    path('todos/<int:pk>', TodoDetailView.as_view(), name='info'),
    path('todos/create', TodoCreateView.as_view(), name='create'),
    path('todos/<int:pk>/update', TodoUpdateView.as_view(), name='update'),
    path('todos/<int:pk>/delete', TodoDeleteView.as_view(), name='delete'),
]
