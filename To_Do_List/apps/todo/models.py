from django.contrib.auth import get_user_model
from django.db import models

from django.conf import settings


class ToDo(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='todo/%Y/%m/%d', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='todo/%Y/%m/%d/thumbnail', default="default/todo_default.png", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'todos'
        verbose_name = '할 일'
        verbose_name_plural = '할 일 목록'


class Comment(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.todo.title}"

    class Meta:
        db_table = 'comments'
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'

