from django.urls import path
from apps.todo_list.views import *

urlpatterns = [
    path('todos/', todo_list, name='todo_list'),
    path('todos/<int:todo_id>/', todo_info, name='todo_info'),
]