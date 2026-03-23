from django.urls import path
from apps.todo.cbvs import *


app_name = 'cbv_todo'

urlpatterns = [
    # ToDo
    path('todos/', ToDoListView.as_view(), name='list'),
    path('todos/<int:todo_id>', TodoDetailView.as_view(), name='info'),
    path('todos/create', TodoCreateView.as_view(), name='create'),
    path('todos/<int:todo_id>/update', TodoUpdateView.as_view(), name='update'),
    path('todos/<int:todo_id>/delete', TodoDeleteView.as_view(), name='delete'),

    # Comment
    path('comments/<int:todo_id>/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
