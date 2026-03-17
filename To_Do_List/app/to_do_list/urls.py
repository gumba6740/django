from django.urls import path
from app.to_do_list.views import *

urlpatterns = [
    path('todo/', todo_list),
    path('todo/<int:todo_id>/', todo_info),
]