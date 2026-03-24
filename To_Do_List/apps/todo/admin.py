from django.contrib import admin

from apps.todo.models import ToDoList, Comment


admin.site.register(Comment)
class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['message', 'user', 'todo']


@admin.register(ToDoList)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'is_completed', 'start_date', 'end_date']
    list_display_links = ['title', 'description', 'is_completed', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date', 'is_completed']
    inlines = [
        CommentInline,
    ]

